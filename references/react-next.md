# React e Next.js

## Orientamento specifico

- **Versione di React** (`react` nel lockfile). `<Activity>` e `useEffectEvent` esistono da React 19.2: non proporli su versioni precedenti.
- **React Compiler** attivo? Cerca `babel-plugin-react-compiler` o l'opzione del compilatore nella configurazione di Next o del bundler. Se è attivo, la memoizzazione manuale (`memo`, `useMemo`, `useCallback`, JSX statico estratto) non serve: non aggiungerla e non segnalarne l'assenza.
- **Versione di Next.js** e router (App Router in `app/`, Pages Router in `pages/`).
  - Da Next 16.3 la documentazione della versione installata è in `node_modules/next/dist/docs/`, e `next dev` genera un `AGENTS.md` che la richiama. **È la fonte primaria per le API di Next**: consultala prima di affidarti a questa skill o alla memoria.
  - Su versioni precedenti esiste un codemod che scarica la documentazione nel progetto. Esegue codice remoto, quindi **proponilo all'utente**, non lanciarlo di tua iniziativa.
- **Librerie già presenti** per dati (SWR, TanStack Query…), stato nell'URL, virtualizzazione, form, animazioni: si usano quelle. Introdurne una nuova è una decisione da proporre.

## Errori frequenti di Next.js (verificare sulla doc della versione)

- **Confini tra server e client**: niente componenti client `async`; le prop passate da server a client devono essere serializzabili; `'use client'` il più in basso possibile nell'albero.
- **API di richiesta asincrone** (`params`, `searchParams`, `cookies()`, `headers()`): vanno attese dalla versione 15.
- **Next 16**: la convenzione `middleware` è deprecata e rinominata `proxy`; su `next/image` la prop `priority` è deprecata a favore di `preload`.
- Metadata con l'API dedicata, non con tag scritti a mano nel `<head>`; font con `next/font`; confini di errore e not-found con le convenzioni di file del router.
- Le **server action sono endpoint pubblici**: autentica e autorizza dentro ciascuna, come faresti in una route API.

## Regole ordinate per impatto

Applica prima le categorie più in alto. Quelle basse contano solo nei percorsi caldi che la profilazione ha mostrato lenti.

### 1. Eliminare le cascate di richieste — critico
- Avvia insieme le operazioni indipendenti e attendile insieme (`Promise.all`), invece di attenderle una dopo l'altra.
- Sposta l'`await` nel ramo che usa davvero il valore; controlla prima le condizioni sincrone economiche.
- Nelle route e negli handler avvia le promesse presto e attendile tardi.
- Ristruttura l'albero dei server component perché i fetch indipendenti partano in parallelo; usa `Suspense` per mandare in streaming le parti lente invece di bloccare la pagina.

### 2. Dimensione del bundle — critico
- Import diretti invece che dai file barile nei percorsi caldi, salvo ottimizzazione configurata e verificata.
- Import dinamico per componenti pesanti o condizionali; moduli caricati solo quando la funzione viene attivata.
- Terze parti (analytics, logging) dopo l'hydration.
- Preload all'intenzione (hover, focus).
- Percorsi di import e di file staticamente analizzabili, per non trascinare nel bundle intere cartelle.

### 3. Server — alto
- **Mai stato mutabile a livello di modulo per dati della richiesta**: i render lato server sono concorrenti nello stesso processo, e i dati di un utente finirebbero nella risposta di un altro. Il livello di modulo va bene solo per configurazione immutabile, asset statici e cache pensate apposta, con chiavi corrette.
- Deduplica per richiesta con `React.cache()`; per la cache tra richieste usa ciò che il progetto già usa, con chiavi corrette.
- Passa ai componenti client solo i dati che usano, senza duplicarli tra prop diverse.
- Lavoro non bloccante dopo la risposta (log, analytics) con `after()` dove la versione lo supporta.

### 4. Dati lato client — medio-alto
- Deduplica le richieste con la libreria dati del progetto.
- Listener globali deduplicati; listener di scroll e touch passivi.
- Dati in `localStorage` versionati e minimi, con letture messe in cache.

### 5. Re-render — medio
- **Deriva durante il render**, non in un effetto che copia dati nello stato.
- Logica di interazione nei gestori di evento, non in effetti che reagiscono a uno stato impostato dal gestore.
- `setState` funzionale quando il nuovo stato dipende dal precedente; inizializzazione pigra (`useState(() => …)`) per valori costosi.
- **Mai definire componenti dentro altri componenti**: vengono rimontati a ogni render e perdono stato e focus.
- Dipendenze primitive negli effetti; sottoscrivi valori derivati (un booleano) invece del valore grezzo quando basta.
- `startTransition` o `useDeferredValue` per aggiornamenti non urgenti che rallentano l'input.
- Ref per valori transitori e frequenti che non devono causare render.
- Memoizzazione manuale solo senza React Compiler e solo dove una misura mostra il costo.

### 6. Rendering — medio
- Condizioni esplicite: `{count > 0 ? <Badge /> : null}`, non `{count && <Badge />}`, che renderizza `0`.
- `content-visibility: auto` o virtualizzazione per liste lunghe.
- Anima un contenitore invece dell'elemento SVG; riduci la precisione delle coordinate SVG generate.
- Mismatch di hydration: per dati disponibili solo sul client usa uno script inline che imposta il valore prima del paint, oppure un rendering solo client esplicito; sopprimi l'avviso solo dove è inevitabile.
- `<Activity>` (React 19.2+) per nascondere e mostrare conservando lo stato.
- Resource hint con le API di React DOM (`preload`, `preconnect`…) invece di tag scritti a mano.

### 7. JavaScript — basso, solo nei percorsi caldi
Map e Set per ricerche ripetute, un'unica iterazione al posto di catene di `filter` e `map`, uscite anticipate, espressioni regolari fuori dai cicli, `toSorted()` per non mutare, lavoro non critico in `requestIdleCallback`.

## Verifica

Typecheck e build con gli script del progetto; test esistenti (Vitest o Jest con Testing Library, Playwright). Con Next 16.3+ e Turbopack, se il progetto usa l'endpoint MCP di sviluppo di Next.js o la skill ufficiale di verifica del ciclo di sviluppo, preferiscili per gli errori di compilazione e di runtime.
