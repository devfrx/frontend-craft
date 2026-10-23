---
name: frontend-craft
description: Progettare, costruire, rivedere e verificare interfacce frontend di qualità da produzione, coerenti con il progetto — direzione visiva non generica, riuso del design system, accessibilità WCAG 2.2 AA, Core Web Vitals, React/Next.js, Vue, Angular, shadcn/ui, da Figma a codice, verifica nel browser. Usa questa skill OGNI VOLTA che un task crea o modifica UI (pagine, landing, dashboard, componenti, form, stati vuoti o di errore, stile, tema, tipografia, colori, animazioni, copy dell'interfaccia) e quando l'utente chiede di rivedere, criticare, rifinire o fare un audit di una UI, sistemare accessibilità o performance frontend, implementare un design Figma o controllare una pagina nel browser — anche se non nomina mai design o qualità. Non usarla per backend, API o logica senza interfaccia.
---

# Frontend Craft

Questa skill governa il lavoro sulle interfacce: dalla direzione visiva alla verifica nel browser. È la sintesi verificata delle migliori skill frontend esistenti (Anthropic, Vercel, Addy Osmani, Impeccable, shadcn, Figma, Angular, Vue): ne tiene il meglio, corregge ciò che le fonti primarie smentiscono e risolve i punti in cui si contraddicono. Provenienza e scelte sono in `FONTI.md`.

Il problema che risolve: le UI prodotte da un agente falliscono quasi sempre in uno di tre modi. **Sembrano generiche**, perché ricadono negli stessi default. **Ignorano il progetto**, e reinventano componenti, usano colori raw o API di una versione diversa da quella installata. **Dichiarano una qualità mai misurata**: "accessibile", "veloce", "responsive" scritti senza aver guardato. Ogni fase qui sotto esiste per chiudere uno di questi tre buchi.

## Rapporto con le altre skill

- **decision-principles** sta sotto questa skill e ne governa il modo di decidere.
- **dev-discipline** e **dev-communication** governano il lavoro sul codice in generale. Questa skill ne è la specializzazione sull'interfaccia: sul dominio UI vale questa, sul resto quelle.
- **design-docs** decide dove vivono mockup, diagrammi e ADR. Una nuova libreria UI, di animazione, di stato o di componenti è una decisione architetturale: si propone e si documenta lì.
- **Skill ufficiali di un framework o di uno strumento** già installate (ad esempio quelle di Angular, di Next.js o di Figma MCP) hanno la precedenza sulle API e sulla meccanica dei loro strumenti, perché sono versionate con il framework. Qui restano valide le regole di qualità, direzione e verifica.
- **frontend-design** (Anthropic): i suoi principi sono inclusi ed estesi in `references/direzione-visiva.md`. Se è caricata insieme a questa non c'è conflitto; dove questa è più specifica, vale questa.
- **Skill di design invocabili come comando** (critique, accessibility review, ux copy, design system): se l'utente ne invoca una esplicitamente, eseguila. Senza invocazione esplicita, per il lavoro frontend usa questa.

Se in un caso concreto questa skill e un'altra dicono cose diverse, esegui secondo la più specifica e **segnala la divergenza** all'utente invece di risolverla in silenzio.

## Principi, in ordine di precedenza

1. **Il progetto è la fonte di verità.** Versione del framework, design system, token, componenti, convenzioni di copy, i18n e test si leggono nel repo prima di scrivere una riga. Le regole di questa skill sono il default quando il progetto tace, non una correzione del progetto. Se una convenzione del progetto contraddice lo stato dell'arte, segui la convenzione e segnala la divergenza.
2. **Il brief vince sul gusto.** Un'indicazione esplicita (palette, font, epoca, stile, riferimenti) si segue anche quando coincide con un default che altrimenti eviteresti. *Rifinire preserva*: identità, comportamento, copy e tutto ciò che è fuori scope restano come sono. *Ridisegnare sostituisce*: il vecchio aspetto diventa un'anti-referenza, ma contenuti, funzioni e vincoli restano. Mai la via di mezzo, cioè lucidare un look che si sta scartando.
3. **Evidenza, non intenzione.** Contrasto, metriche, accessibilità e resa visiva sono affermazioni verificabili: si misurano. Senza evidenza runtime si scrive "causa probabile", non "fallisce". In consegna si separano sempre il verificato, il dedotto e l'assunto.
4. **Passate limitate.** Costruisci per intero, poi ispeziona in una sola passata raggruppata (desktop e mobile, stati principali, tastiera), correggi tutto in blocco e conferma con al massimo una seconda passata. Poi fermati e riporta ciò che resta aperto. L'auto-revisione senza fine costa e non migliora il risultato.
5. **Scope stretto.** Le discrepanze trovate fuori dallo scope del task si annotano, non si correggono. Una nuova dipendenza è una decisione da proporre, non un dettaglio implementativo.
6. **Nessuna esecuzione implicita.** Questa skill non scarica regole remote, non esegue pacchetti `@latest` per conto suo, non installa binari e non costruisce comandi shell da stringhe non fidate. CLI di librerie e strumenti di automazione del browser si usano solo se sono già nel progetto (alla versione fissata lì) o con il consenso esplicito dell'utente.

## Workflow

### 0. Orientamento (sempre)

Leggi prima di decidere. È lavoro di pochi minuti che evita la maggior parte degli errori.

- **Stack e versioni**: `package.json` e lockfile. Framework e versione esatta, libreria di componenti, sistema di stile (Tailwind 3 con `tailwind.config.*` o Tailwind 4 con `@theme` nel CSS, CSS Modules, altro), stato, form, i18n, test unitari ed E2E.
- **Design system**: token (custom property CSS, `@theme`, file di tema), componenti condivisi (`components/ui/`, pacchetto interno, Storybook), `components.json` se il progetto usa shadcn/ui.
- **Convenzioni**: linter, formatter e stylelint; lingua e tono della UI esistente (maiuscole, virgolette, formati di date e numeri); struttura delle cartelle e naming.
- **Documentazione di design**: `docs/design/`, ADR, `DESIGN.md` o `PRODUCT.md` se esistono.
- **Documentazione versionata del framework**: con Next.js 16.3 o superiore, `node_modules/next/dist/docs/` e l'`AGENTS.md` generato da `next dev`. Per gli altri framework, la documentazione ufficiale della versione installata.

Chiudi l'orientamento classificando il task con la tabella seguente e annotando in 3-5 righe ciò che hai trovato. Quelle righe sono il contesto che il resto del lavoro deve rispettare.

### Cosa leggere, per tipo di task

| Task | Leggi, in quest'ordine |
|---|---|
| UI nuova o redesign | `references/direzione-visiva.md` → `references/pavimento-qualita.md` → reference del framework |
| Rifinire o estendere UI esistente | `references/pavimento-qualita.md` → reference del framework → `references/design-system.md` se tocchi componenti condivisi |
| Review, critica o audit di UI | `references/review-ui.md` (+ `accessibilita.md` o `performance.md` se in scope) |
| Accessibilità | `references/accessibilita.md` |
| Performance e Core Web Vitals | `references/performance.md` |
| Da Figma a codice | `references/design-system.md` (sezione Figma) → `references/pavimento-qualita.md` |
| Verifica nel browser, test E2E | `references/verifica-browser.md` |

Reference per framework, da leggere solo quello dello stack in uso: `references/react-next.md`, `references/vue.md`, `references/angular.md`. Per qualsiasi design system, shadcn/ui compreso, `references/design-system.md`.

### 1. Direzione (solo UI nuova o redesign)

Il percorso è: brief → modalità della superficie → piano di token compatto → confronto del piano con i default ricorrenti → codice. Se il brief non dice qual è il soggetto, per chi è o qual è il compito principale della pagina, proponi un'ipotesi concreta e falla confermare prima di costruire. Il dettaglio è in `references/direzione-visiva.md`.

### 2. Costruzione

- **Riusa nell'ordine**: componente o variante esistente → composizione di componenti esistenti → token nuovo nel sistema → componente nuovo che segue le convenzioni del sistema (e lo segnali). Mai colori raw al posto dei token, mai `z-index` manuali sugli overlay del sistema.
- **Applica il pavimento di qualità** (`references/pavimento-qualita.md`) senza annunciarlo: stati, contenuti reali, responsive, tastiera, semantica.
- **Copy** nella lingua, nel tono e con la terminologia del prodotto. Contenuti reali o verosimili, mai inventare dati o affermazioni.
- **Test**: se il progetto ha test di componente o E2E, aggiungili o aggiornali nello stesso stile.

### 3. Revisione

Scrivi prima il giudizio di design (specificità, gerarchia, flusso) e solo dopo passa la checklist meccanica: in quest'ordine la checklist non condiziona il giudizio. I findings vanno in formato `file:riga` con severità. Metodo e formato sono in `references/review-ui.md`.

### 4. Verifica

- **Build e tipi** con gli script del progetto (`tsc`, `vue-tsc`, `ng build`, `next build` o equivalenti), più lint e test esistenti.
- **Browser** con lo strumento disponibile: render desktop e mobile, stati, percorso da tastiera, reduced motion, tema scuro se supportato. Vedi `references/verifica-browser.md`.
- **Contrasto** misurato con lo script incluso, non stimato.
- Se non c'è un browser disponibile, dillo esplicitamente ed elenca cosa resta da verificare e come farlo.

### 5. Consegna

Chiudi sempre con questo schema, omettendo le sezioni vuote:

```
Fatto: <cosa è cambiato, file principali>
Verificato: <cosa, con quale strumento e in quali condizioni>
Dedotto o non verificato: <cosa, e perché non è stato possibile verificarlo>
Fuori scope (annotato, non toccato): <file:riga — problema>
Da decidere: <nuove dipendenze, scelte che richiedono conferma>
Documentazione di design: <aggiornata / da aggiornare secondo design-docs>
```

## Severità, unica per tutta la skill

| Livello | Significato | Esempi |
|---|---|---|
| P0 | Blocca il task o esclude una categoria di utenti | Form non inviabile da tastiera, azione primaria invisibile su mobile |
| P1 | Difficoltà seria o violazione WCAG AA | Contrasto insufficiente, campo senza label, focus invisibile |
| P2 | Fastidio con una via d'uscita | Stato di caricamento assente, troncamento brutto |
| P3 | Rifinitura | Spaziatura incoerente, numeri non tabulari |

Nel dubbio tra due livelli chiediti: *un utente contatterebbe l'assistenza per questo?* Se sì, è almeno P1.

## Strumento incluso: contrasto

`scripts/contrasto.py` calcola il rapporto WCAG tra due colori CSS (hex, `rgb()`, `hsl()`, `oklch()`, anche con trasparenza) e dice se supera AA/AAA per testo normale, testo grande e componenti. È offline e senza dipendenze.

```bash
python scripts/contrasto.py '<colore testo>' '<colore sfondo>' [--dimensione PX] [--grassetto] [--ui]
```

Esito: 0 se supera la soglia AA della categoria valutata, 1 se non la supera, 2 per errore d'uso. Passa i valori *calcolati* (da `getComputedStyle` o dai token risolti), non nomi di variabile. Test: `python -m unittest discover -s scripts -p "test_*.py"`.
