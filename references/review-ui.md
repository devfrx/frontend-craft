# Review, critica e audit di UI

## Metodo

1. **Risolvi il bersaglio**: file o route precisi. "La home" diventa il file della pagina, "la modale delle impostazioni" il suo componente. Se l'utente non indica cosa rivedere, chiedilo.
2. **Leggi il contesto del progetto** come nell'orientamento di `SKILL.md`. Un colore raw in un progetto senza token non è lo stesso finding di un colore raw in un progetto che ne ha 200.
3. **Giudizio di design per primo, scritto.** Scrivi il giudizio (sezione sotto) prima di passare la checklist. Se l'ambiente offre sotto-agenti, puoi affidare giudizio e checklist a due passate indipendenti; altrimenti rispetta l'ordine e dichiaralo nel report.
4. **Checklist meccanica**: `pavimento-qualita.md`, più i segnali nel codice qui sotto, più `accessibilita.md` e `performance.md` se sono nello scope.
5. **Evidenza nel browser** se disponibile (`verifica-browser.md`). Tieni separati i findings deterministici (trovati nel codice o misurati) dal giudizio, e segnala i falsi positivi.
6. **Report** nel formato in fondo. Poi fermati: una review non corregge, salvo richiesta esplicita.

## Giudizio di design

### Specificità
Il risultato sembra fatto per questo prodotto o potrebbe usarlo, identico, un prodotto qualsiasi? Controlla i default di `direzione-visiva.md` (sezione 4), tenendo presente che se il brief o il progetto li hanno scelti non sono un difetto.

### Carico cognitivo
Conta quanti degli otto controlli falliscono:
- un compito principale, senza elementi concorrenti;
- informazioni in gruppi di al massimo quattro elementi;
- elementi correlati raggruppati visivamente;
- gerarchia che rende evidente cosa conta di più;
- una decisione alla volta;
- al massimo quattro opzioni visibili in un punto di scelta;
- nessuna informazione da ricordare da una schermata precedente;
- complessità rivelata solo quando serve.

0-1 fallimenti: carico basso. 2-3: moderato, da affrontare. 4 o più: alto, è un problema critico.

La memoria di lavoro regge circa quattro elementi. Per esempio: un'azione primaria e una o due secondarie, il resto in un menu; non più di cinque voci di navigazione di primo livello.

### Euristiche di Nielsen (per una critica completa)
Punteggio da 0 a 4 per ciascuna: visibilità dello stato del sistema, corrispondenza con il mondo reale, controllo e libertà dell'utente, coerenza e standard, prevenzione degli errori, riconoscimento anziché ricordo, flessibilità ed efficienza, design essenziale, recupero dagli errori, aiuto e documentazione.

Un 4 significa davvero eccellente; la maggior parte delle interfacce reali sta tra 20 e 32 su 40. Sulle superfici Persuadere ed Esperienza le euristiche non pertinenti (tipicamente flessibilità e documentazione) si segnano `n/a` con una riga di motivazione, e il totale si rapporta al massimo applicabile. Fasce in percentuale: 90% eccellente, 70% buono, 50% accettabile, 30% scarso, sotto critico.

### Personas
Scegli le due o tre più pertinenti e percorri l'azione principale con ciascuna, nominando cosa si rompe:
- **utente esperto e impaziente**: cerca scorciatoie da tastiera, azioni in blocco, pochi clic;
- **utente alla prima visita**: si perde con icone senza etichetta, gergo, aiuto assente;
- **utente con tecnologie assistive**: screen reader, solo tastiera, zoom, contrasto elevato;
- **collaudatore ostinato**: input estremi, doppi clic, rete lenta, stati vuoti ed errori;
- **utente mobile distratto**: una mano, interruzioni, target piccoli, connessione instabile.

Scrivi cosa si è rotto per ciascuno, non una descrizione generica della persona.

## Segnali nel codice

Pattern concreti da cercare. Ognuno è un finding salvo giustificazione visibile nel contesto.

**Accessibilità e semantica**
- `<div>` o `<span>` con `onClick` / `@click` / `(click)`.
- Navigazione fatta con un gestore di clic invece che con un link.
- `<button>` o link con sola icona e senza nome accessibile.
- `<img>` senza `alt`; icone decorative senza `aria-hidden`.
- Input senza label associata; placeholder usato come label.
- Toast e validazioni asincrone senza regione `aria-live`.
- Gestori da tastiera aggiunti a elementi nativi (`<button>`, `<a>`): provocano doppia attivazione. Servono solo su elementi non nativi con `role` e `tabindex`.
- `user-scalable=no` o `maximum-scale=1` nel viewport.

**Focus e interazione**
- `outline: none` / `outline-none` senza un sostituto `:focus-visible`.
- `:focus` usato dove serve `:focus-visible`.
- `onPaste` con `preventDefault`.
- `autoFocus` senza giustificazione.
- Azione disponibile solo tramite gesto.

**Stile e motion**
- `transition: all` / `transition-all`.
- Animazioni di `width`, `height`, `top`, `left`, `margin` per effetti che `transform` otterrebbe.
- Assenza di `prefers-reduced-motion` accanto ad animazioni non banali.
- Colori raw dove esistono token; `dark:` manuali che duplicano token semantici; `z-index` manuali su overlay del sistema.
- `will-change` lasciato attivo a riposo o applicato in modo diffuso.

**Contenuti e formati**
- Date, numeri o valute formattati a mano invece che con `Intl.*` o la libreria del progetto.
- `...` al posto di `…` nei testi dell'interfaccia; maiuscole incoerenti con la convenzione del progetto.
- Messaggi di errore che descrivono il problema senza dire come rimediare; etichette vaghe ("Continua", "Invia", "OK").

**Rendering e performance**
- `<img>` senza dimensioni.
- Liste molto lunghe renderizzate per intero senza virtualizzazione o `content-visibility`.
- Letture di layout (`getBoundingClientRect`, `offsetHeight`, `scrollTop`) nel render o alternate a scritture.
- GIF animate dove basterebbe un video.
- In React: `{count && …}` con un numero come condizione (renderizza `0`).

## Formato del report

```
## Giudizio di design
<3-6 righe: specificità, cosa funziona e perché, il problema principale>
<tabella delle euristiche solo per una critica completa>

## Findings
### src/components/SettingsForm.tsx
src/components/SettingsForm.tsx:42 [P1] bottone solo icona senza nome accessibile
src/components/SettingsForm.tsx:67 [P2] transition: all → elencare le proprietà
src/components/SettingsForm.tsx:88 [P1] errore mostrato solo in rosso, senza testo né aria-invalid

### src/components/Card.tsx
✓ nessun problema

## Fuori scope (annotato, non toccato)
## Non verificato
<cosa, e con quale strumento andrebbe verificato>
```

Regole di scrittura: problema e posizione, spiegazione solo se la correzione non è ovvia, nessun preambolo. Ordina i file per severità massima. Chiudi con al massimo due o tre domande che potrebbero sbloccare soluzioni migliori, solo se servono davvero.
