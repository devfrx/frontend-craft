# Direzione visiva

Da leggere per una UI nuova o un redesign, prima di scrivere codice. Per una rifinitura di UI esistente non serve: lì l'identità visiva è già decisa e va preservata.

## Indice
1. Radicare nel soggetto
2. Modalità della superficie
3. Piano in due passate
4. Default da riconoscere
5. Tipografia
6. Colore
7. Layout e spazio
8. Motion
9. Parole
10. Moderazione

## 1. Radicare nel soggetto

Le scelte distintive nascono dal mondo del soggetto: il suo settore, i materiali, il lessico, il pubblico. Un sito per un laboratorio di ceramica e una dashboard per analisti finanziari non devono potersi scambiare la palette.

Se il brief non dice cosa sia il prodotto, per chi sia e quale sia il compito principale della pagina, formula un'ipotesi concreta (un soggetto, un pubblico, un compito) e falla confermare prima di costruire. Usa i contenuti reali del brief ovunque.

## 2. Modalità della superficie

La modalità descrive che cosa significa successo per chi visita *quella* superficie. Si sceglie dalla superficie, non dal prodotto: la landing di uno strumento tecnico è comunque Persuadere, la documentazione di una casa di moda è comunque Leggere.

| Modalità | Chi visita vuole | Implicazioni |
|---|---|---|
| **Persuadere** (landing, marketing, pricing, campagne) | decidere e agire | Il design è il prodotto. La tipografia display può portare la voce, un momento di motion orchestrato è benvenuto, le immagini reali contano. |
| **Operare** (app, dashboard, editor, admin, impostazioni) | completare un compito | Leggibilità, densità stabile, coerenza e convenzioni della piattaforma prima dell'espressione. Il brand vive nei dettagli precisi. Motion solo come feedback, veloce. |
| **Leggere** (documentazione, articoli, guide, changelog) | capire | Struttura per la comprensione, misura di riga corretta, un solo percorso di lettura. Poi rendere la lettura piacevole. |
| **Esperienza** (portfolio, gallerie, vetrine) | stare dentro l'opera | L'opera guida dal primo viewport; l'interfaccia si ritrae. |

## 3. Piano in due passate

**Prima passata: un sistema di token compatto.**
- *Colore*: 4-6 valori nominati (hex o oklch, coerenti con il formato dei token del progetto).
- *Tipografia*: una o due famiglie, con il ruolo di ciascuna.
- *Layout*: il concetto in una frase, con wireframe ASCII per confrontare alternative. Dichiara l'allineamento (a sinistra, centrato, giustificato).
- *Principi*: due o tre regole che rendono questa pagina specifica.

**Seconda passata: revisione contro il brief.** Per ogni parte del piano chiediti se ci arriveresti con qualsiasi brief simile. Se sì, è un default e non una scelta: rivedi quella parte e dichiara cosa hai cambiato e perché. Solo dopo scrivi il codice.

## 4. Default da riconoscere

Sono i tratti in cui ricade la UI generata in serie. Nessuno è vietato in assoluto: **se il brief o il progetto li chiedono, si usano**. Se invece l'asse è libero, non spendere quella libertà su un default. Quando ne riconosci uno, riscrivi l'elemento; attenuarlo non basta.

**Palette ricorrenti**
- Fondo crema caldo (intorno a `#F4F1EA`) con serif display ad alto contrasto e accento terracotta. Un accento vicino a `#D97757` è il colore d'interazione di Claude, e su un brief altrui si nota.
- Fondo quasi nero con un solo accento acido (verde lime, vermiglio).
- Quasi-nero tinto (`#0B0B0B`, `#111`) al posto di un nero scelto.

**Impaginazione**
- Il contenuto spezzato in card identiche (icona, titolo, testo), con lo stesso raggio ovunque e la stessa ombra grigia leggera. Card annidate in card sono sempre sbagliate.
- Il modello "hero-metric": numero grande, etichetta piccola, statistiche di contorno, accento sfumato.
- Impaginazione da quotidiano (filetti sottili, raggio zero, colonne dense) usata a prescindere dal soggetto.
- Numerazione delle sezioni (01 / 02 / 03) quando il contenuto non è davvero una sequenza.
- Un'etichetta in maiuscoletto spaziato sopra ogni titolo (eyebrow).
- Stringhe di metadati unite da punti centrati, etichette "PAROLA — frammento", una freccia aggiunta a ogni link o bottone.
- Una modale per un compito che non richiede interruzione né focus protetto.

**Superfici**
- Testo con gradiente: l'enfasi nasce da peso e dimensione.
- Vetro e sfocatura come decorazione.
- Bordo laterale colorato più spesso di 1px su card, callout e alert.
- Ombre dure a offset senza sfocatura fuori da un mondo davvero neobrutalista; alone colorato a offset zero come finta profondità.
- Doppia elevazione: bordo da 1px più ombra ampia sullo stesso elemento. Dichiara l'elevazione una volta sola.
- Sfondi a righe o a griglia senza una ragione nel soggetto (una mappa, un progetto tecnico, uno strumento di misura).
- Monospace come costume "tecnico" invece che per codice, dati o misure.
- Emoji o glifi Unicode al posto di un sistema di icone coerente.
- Tema chiaro o scuro scelto per categoria. Si sceglie dalla scena d'uso: chi usa l'interfaccia, dove, con quale luce.

## 5. Tipografia

- La tipografia porta la personalità della pagina. Usa una o due famiglie; se due, chiaramente distinte. Scegline deliberatamente, non quelle che useresti per qualsiasi progetto, e non un font di sistema come voce display di una pagina con identità propria.
- Scala tipografica chiara, con passi di dimensione e di peso evidenti.
- Misura del testo: 65-75 caratteri per riga. Un serif per il corpo vuole un'interlinea un po' più ampia di un sans.
- Tracking dei titoli non sotto `-0.04em`; tra `-0.02em` e `-0.03em` di solito si legge meglio. Titoli bilanciati con `text-wrap: balance`, paragrafi con `text-wrap: pretty`.
- Numeri tabulari (`font-variant-numeric: tabular-nums`) in tabelle, confronti, contatori.
- Da evitare: una sola parola del titolo in corsivo, grassetto o colore diverso; maiuscolo per le etichette; etichette tipografiche superflue sopra i contenuti.
- Font self-hosted o tramite lo strumento del framework (ad esempio `next/font`), con fallback metricamente compatibile per non causare layout shift.

## 6. Colore

- Palette nominata ed espressa come token semantici (`--surface`, `--text-muted`, `--accent`), mai valori raw sparsi nei componenti.
- Su superfici colorate il testo secondario si tinge dalla tinta della superficie o del primo piano, non con un grigio neutro.
- Contrasto misurato con `scripts/contrasto.py` in ogni tema supportato. Soglie in `accessibilita.md`.
- Se il progetto supporta tema chiaro e scuro, progetta entrambi: il tema scuro non è l'inversione di quello chiaro.

## 7. Layout e spazio

- La struttura visiva è informazione. Bordi, numerazioni, etichette e divisori devono codificare qualcosa del contenuto, non decorarlo.
- Gruppi stretti, separazioni generose, più spazio sopra un titolo che sotto.
- Una card si usa solo quando il contenuto è davvero un oggetto a sé.
- Attenzione alla specificità CSS: classi di sezione e classi di componente che si annullano a vicenda sono un errore frequente, soprattutto su padding e margini tra sezioni.

## 8. Motion

- **Un momento orchestrato** (una sequenza al caricamento, una rivelazione) vale più di effetti sparsi. Un'entrata identica su ogni sezione e un hover su ogni card sono il default generato.
- Il motion che risponde a un'azione dell'utente (aprire, espandere, confermare) è benvenuto quando mostra cosa è cambiato.
- Durate indicative:

| Durata | Uso tipico |
|---|---|
| 100-150 ms | feedback immediato |
| 150-300 ms | cambio di stato ordinario |
| 300-500 ms | layout, overlay, transizione di vista |
| 500-800 ms | un'entrata focale deliberata |

- L'uscita è più rapida dell'entrata. Decelerazione naturale, ad esempio `cubic-bezier(0.16, 1, 0.3, 1)`; niente curve elastiche o a rimbalzo per riflesso.
- Il contenuto è visibile nello stato di default: se uno script fallisce, la pagina non deve restare nascosta.
- Di default si animano solo `transform` e `opacity`. Sfocature, filtri, maschere, `clip-path` e ombre si usano solo su regioni limitate e dopo aver misurato che restano fluidi sui dispositivi target. Mai `transition: all`.
- Si usa lo strumento che il progetto ha già (transizioni CSS, Web Animations API, View Transitions, la libreria di motion installata). Non si aggiunge una dipendenza per un effetto che lo stack esprime già.
- In Operare e Leggere nessuna coreografia al caricamento: l'utente non deve aspettare l'animazione.
- Reduced motion: vedi `accessibilita.md`.

## 9. Parole

Le parole di un'interfaccia sono materiale di design, non decorazione.

- Scrivi dalla prospettiva dell'utente e nomina le cose come le capisce lui: "gestisci le notifiche", non "configura i webhook".
- Voce attiva. Un bottone dice esattamente cosa succede ("Salva modifiche", non "Invia"). La stessa azione ha lo stesso nome in tutto il flusso: il bottone "Pubblica" produce un avviso "Pubblicato".
- Gli errori dicono cosa è successo e come rimediare, con la voce dell'interfaccia: niente scuse, niente vaghezza. Uno stato vuoto è un invito ad agire.
- Niente riempitivi, un compito per ogni elemento di testo. Descrivere, non vendere.
- **Maiuscole**: segui la convenzione del progetto. Se non esiste, usa sentence case. In italiano sempre sentence case: il Title Case non è una convenzione italiana.
- **Tipografia del testo secondo la lingua**: ellissi vera (`…`) anche negli stati di caricamento ("Caricamento…"); virgolette curve in inglese, in italiano quelle dello stile della casa (« » oppure “ ”); spazio non separabile tra numero e unità (`10&nbsp;MB`); numerali per i conteggi ("8 progetti").
- Contenuti reali o verosimili, mai lorem ipsum. I valori illustrativi si etichettano come tali; non si inventano dati, recensioni o affermazioni sul prodotto.

## 10. Moderazione

Spendi l'audacia in un solo punto: un elemento memorabile, tutto il resto tranquillo e disciplinato. Prima di consegnare, togli un accessorio. Il pavimento di qualità (`pavimento-qualita.md`) garantisce la meccanica ma non sceglie la direzione: con tutti i controlli superati, investi nel mondo che hai scelto.
