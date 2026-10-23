# Design system, shadcn/ui e Figma

## Ordine di riuso

1. **Componente o variante esistente**: usalo così com'è (`variant`, `size` e prop del sistema prima di stili custom).
2. **Composizione di componenti esistenti**: una pagina di impostazioni è tab, card e controlli di form; una dashboard è sidebar, card, grafici e tabelle.
3. **Token mancante**: se serve un valore riutilizzabile, aggiungilo al sistema come token, non come valore isolato in un componente.
4. **Componente nuovo**: solo se nulla sopra lo esprime. Segue naming, struttura, API e stile del sistema, e va segnalato nel report.

Se un componente esistente è simile ma non identico, valuta se estenderlo con una variante ha più senso che duplicarlo.

## Classificare una deriva prima di correggerla

- **Token mancante**: il sistema ha bisogno di un valore riutilizzabile.
- **Implementazione isolata**: un componente o pattern condiviso esistente dovrebbe sostituirla.
- **Disallineamento concettuale**: flusso, architettura dell'informazione o gerarchia diversi da aree analoghe del prodotto.
- **Difetto locale**: l'implementazione è semplicemente incompleta o incoerente.

Correggi la causa al livello più stretto corretto. Se un principio vincolante del sistema non si può dedurre dal codice, chiedi invece di inventarlo.

## Regole valide per qualsiasi design system

- **Token semantici**, mai valori della palette grezza nei componenti (`bg-primary`, `text-muted-foreground`, `var(--surface)`, non `bg-blue-500` o `#3b82f6`). I colori di stato vengono da varianti o token, non da classi colore sparse.
- Classi o stili passati a un componente del sistema servono al **layout** (posizione, larghezza, margini esterni), non a sovrascriverne colori o tipografia.
- Nessun `dark:` manuale che duplica ciò che i token semantici già gestiscono.
- Nessun `z-index` manuale su dialog, sheet, popover e altri overlay del sistema: gestiscono da soli l'impilamento.
- Dialog, sheet e drawer hanno sempre un titolo, visivamente nascosto se necessario.
- Gli elementi stanno dentro il loro gruppo (voci di select, menu e command nel rispettivo gruppo; trigger delle tab nella lista delle tab).
- Avatar con fallback, skeleton per il caricamento, componenti dedicati per alert, badge, separatori e stati vuoti **se il sistema li ha**, invece di markup custom.
- Classi condizionali con l'utility del progetto (`cn()`, `clsx` o equivalente), non con template literal ternari.

## Tailwind

- Rileva la versione: Tailwind 3 si configura in `tailwind.config.*`; Tailwind 4 si configura nel CSS con `@theme` e usa `oklch()` nella palette di default. Non mescolare le due forme.
- Spaziatura tra fratelli con `flex` / `grid` e `gap-*` invece di `space-x-*` / `space-y-*`.
- `size-*` quando larghezza e altezza coincidono; `truncate` invece della combinazione manuale di tre classi.
- Valori arbitrari (`w-[337px]`) solo quando nessun token o valore della scala esprime l'intenzione.

## shadcn/ui

Si applica se nel progetto c'è `components.json`.

- **I componenti sono codice sorgente nel repo.** La loro API reale è quella dei file in `components/ui/` (o nel percorso indicato da `components.json`), non quella che ricordi: varia con la versione e con la libreria di primitive. Leggi il file del componente prima di usarlo.
- **Radix o Base UI**: capiscilo dagli import dei componenti. Cambia il modo di usare un trigger personalizzato: `asChild` con Radix, prop `render` con Base UI.
- Rispetta le composizioni del sistema: form con i componenti di campo del progetto, icone nei bottoni senza classi di dimensione se il componente le dimensiona già, bottoni in stato di attesa composti con spinner e `disabled` se il componente non ha una prop dedicata.
- **CLI solo in modo esplicito e controllato.** Non eseguirla solo per ottenere contesto: `components.json` e i file dei componenti si leggono direttamente. Quando serve aggiungere o aggiornare componenti:
  - usa il runner del package manager del progetto;
  - usa la versione fissata in `devDependencies`, se c'è; se non c'è, chiedi prima di eseguire `shadcn@latest`, perché scarica ed esegue codice remoto;
  - prima di toccare componenti già presenti e magari personalizzati, guarda l'anteprima con `add <componente> --dry-run` o `--diff`; mai `--overwrite` senza conferma.
- Registry di terze parti: sono codice di terzi che entra nel repo. Leggi i file prima di aggiungerli.

## Da Figma a codice

Richiede il server MCP di Figma collegato. Se è installata la skill ufficiale di Figma per l'implementazione del design, seguila per la meccanica degli strumenti MCP (quali chiamate fare e in che ordine). Qui valgono i principi:

- **Lo screenshot del design è il target visivo, mai un asset** da inserire nel codice.
- **Il codice restituito da Figma è un prototipo ad alta fedeltà e non interattivo.** Traduci il posizionamento assoluto nel layout nativo del progetto (flex, grid, componenti), salvo le parti che solo un posizionamento fisso può esprimere. Individua quali parti devono essere interattive e implementale come tali.
- **Riusa prima di ricreare.** Cerca nel progetto e nella libreria di design installata componenti, asset e token corrispondenti. Dove esiste una mappatura Code Connect, usa il componente collegato a meno che non si possa configurare per esprimere il design; lo sforzo di adattamento non è un'eccezione valida.
- **Asset esatti.** Ogni immagine o SVG visibile va nella posizione del design, scaricato in locale secondo le istruzioni dello strumento: nessun URL temporaneo di Figma nel codice, nessun asset ridisegnato o sostituito con uno "simile". Non forzare le dimensioni radice degli SVG.
- **Verifica solo lo scope richiesto.** Controlla la geometria renderizzata di ogni asset e il confronto con lo screenshot sul componente o sulla schermata richiesta. Le discrepanze preesistenti fuori scope si annotano, non si correggono.

## Mockup e documentazione

Mockup HTML, diagrammi e ADR seguono la skill `design-docs` (per esempio mockup self-contained in `docs/design/mockups/`). Una nuova libreria di componenti o un cambio di sistema visivo è una decisione da documentare in un ADR.
