# Pavimento di qualità

Da applicare a ogni UI costruita o modificata, senza annunciarlo. Ogni voce è un controllo **sul risultato costruito**, non un'intenzione: si verifica nella passata di ispezione raggruppata (vedi `verifica-browser.md`). Il brief o il sistema visivo del progetto prevalgono sulle scelte estetiche di questa lista, mai su accessibilità e correttezza.

## Stati

- Ogni elemento interattivo ha gli stati hover, focus visibile, attivo e disabilitato. Gli stati interattivi aumentano il contrasto rispetto a quello di riposo.
- Ogni vista che carica dati ha gli stati di caricamento, errore, vuoto e successo. Uno stato vuoto non è un'interfaccia rotta.
- Un bottone di invio resta abilitato finché la richiesta non parte, poi mostra che è in corso e impedisce il doppio invio.
- Azioni distruttive: conferma o finestra di annullamento, mai effetto immediato.

## Contenuti reali e casi limite

- Testi corti, medi e molto lunghi: nomi di oltre 100 caratteri, parole lunghe senza spazi, emoji.
- Quantità: zero, uno, molti, oltre mille elementi.
- Contenitori di testo che reggono il contenuto lungo con troncamento, `line-clamp` o `overflow-wrap: anywhere`. I figli flex che devono troncare hanno `min-width: 0`.
- Immagini mancanti o lente: il layout non salta e c'è un fallback.
- Se il prodotto supporta altre lingue: testi sensibilmente più lunghi (tedesco, finlandese), scritture da destra a sinistra, CJK.

## Responsive e input

- Da 320px a desktop largo: nessuno scroll orizzontale indesiderato, nessun contenuto tagliato.
- Zoom del testo al 200% senza perdita di contenuto o funzioni; il layout si ridispone a 320px CSS di larghezza.
- Target interattivi di almeno 24×24px (minimo WCAG AA); 44×44px dove l'input principale è il touch.
- Layout a tutto schermo con `env(safe-area-inset-*)`; `overscroll-behavior: contain` su modali, drawer e sheet.
- `touch-action` definito sulle superfici trascinabili. Ogni gesto (trascinare, scorrere, pizzicare) ha un'alternativa con clic o tap e con tastiera.
- `autofocus` solo con una giustificazione chiara: un solo campo primario, su desktop.

## Tastiera e focus

- Tutto è raggiungibile e attivabile da tastiera, in un ordine che segue quello visivo.
- Focus visibile con `:focus-visible`. Mai `outline: none` senza un sostituto con contrasto di almeno 3:1.
- Header, footer e overlay sticky non coprono l'elemento con il focus (`scroll-margin-top` / `scroll-margin-bottom`).
- Nessuna trappola di focus. Le modali gestiscono focus e ritorno del focus: `<dialog>` nativo o la primitiva del design system.
- Controlli composti: focus di gruppo con `:focus-within`.

## Semantica

- `<button>` per le azioni, `<a href>` (o il `Link` del router) per la navigazione, così funzionano Cmd/Ctrl+clic e clic centrale. Mai `<div>` o `<span>` con un gestore di clic.
- Un'etichetta per ogni controllo, titoli in gerarchia, landmark (`header`, `nav`, `main`, `footer`), `lang` su `<html>`, titolo di pagina significativo, link per saltare al contenuto.
- Bottoni con sola icona: nome accessibile. Icone decorative: `aria-hidden="true"`.

## Form

- Label cliccabile (associata o che avvolge il controllo). Il placeholder non sostituisce la label.
- `type` e `inputmode` corretti (`email`, `tel`, `url`, `number`) e `autocomplete` con il token giusto sui dati personali: è un requisito WCAG AA (1.3.5). `name` significativo.
- Mai bloccare l'incolla.
- Controllo ortografico disattivato su email, codici e nomi utente.
- Errori accanto al campo, collegati con `aria-describedby` e segnalati con `aria-invalid`; all'invio il focus va al primo errore.
- Checkbox e radio: label e controllo formano un'unica area cliccabile, senza zone morte.
- Avviso prima di lasciare la pagina con modifiche non salvate, usando il meccanismo del router del progetto.

## Navigazione e stato

- Lo stato che ha senso condividere (filtri, tab, paginazione, pannelli aperti) vive nell'URL, con la soluzione di routing che il progetto già usa.

## Immagini e media

- `width` e `height`, o `aspect-ratio`, su ogni immagine.
- Caricamento lazy sotto la piega; priorità alta sull'elemento LCP usando l'API della **versione installata** del framework (in Next.js 16 `priority` è deprecata a favore di `preload`).
- `alt` significativo, oppure vuoto se l'immagine è decorativa.
- Video compresso (`autoplay muted loop playsinline`) al posto delle GIF animate, con un'immagine ferma alternativa.
- Movimento automatico che dura più di 5 secondi insieme ad altri contenuti: controlli per mettere in pausa, fermare o nascondere.

## Superfici del browser

Le parti che non hai disegnato portano comunque il design, e sono le più trascurate: selezione del testo, cursore di inserimento, scrollbar personalizzate, anello di focus, distanza della sottolineatura, numeri nelle tabelle. Tematizzale dalla palette.

Per il tema scuro servono anche `color-scheme` su `<html>`, `<meta name="theme-color">` coerente con lo sfondo e `background-color`/`color` espliciti sui `<select>` nativi (Windows in tema scuro).

## Tema e token

- Nessun colore, spaziatura o raggio hardcoded dove esiste un token.
- Il tema scuro, se supportato, è completo e ha il contrasto verificato come quello chiaro.
- Il cambio di tema aggiorna tutti i valori, compresi quelli calcolati in JavaScript.

## i18n e formati

- Date, ore, numeri e valute con `Intl.DateTimeFormat` e `Intl.NumberFormat`, oppure con la libreria i18n del progetto. Mai formati hardcoded.
- Nessuna stringa hardcoded se il progetto ha un sistema di traduzione.
- `translate="no"` su nomi di brand, codice e identificatori.
- Lingua dell'utente da `navigator.languages` o `Accept-Language`, non dall'IP.

## Rendering lato server e hydration

- Input con `value` hanno anche il gestore di modifica, oppure usano `defaultValue`.
- Date e ore dipendenti dal client protette da mismatch di hydration.
- Soppressione degli avvisi di hydration solo dove è davvero inevitabile.

## Motion

- Esiste un comportamento con `prefers-reduced-motion` (dettagli in `accessibilita.md`).
- Nessun `transition: all`; `transform-origin` corretto; animazioni interrompibili dall'input.

## Copertura e pulizia

- Ogni requisito del brief è presente e trovabile in pochi secondi.
- Copy nella lingua e con la terminologia del prodotto; i controlli nominano la propria azione.
- Niente codice morto, `console.log`, commenti fuorvianti o classi CSS che si annullano a vicenda.
