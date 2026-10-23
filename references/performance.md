# Performance e Core Web Vitals

Principi indipendenti dal framework. Le regole specifiche di React e Next.js sono in `react-next.md`.

## Misura prima di ottimizzare

Con un URL eseguibile:
1. **Dati di campo** (CrUX al 75° percentile per la pagina, altrimenti per l'origine, dichiarandolo; oppure il RUM del progetto) per capire se c'è un problema reale e quale metrica riguarda.
2. **Traccia del browser** in condizioni dichiarate (dispositivo, rete, cache): con Chrome DevTools MCP se disponibile, altrimenti Lighthouse o PageSpeed Insights come laboratorio.
3. Analizza solo gli insight della metrica che fallisce, poi il codice e le risorse coinvolte.
4. Dopo la correzione ripeti la misura di laboratorio **nelle stesse condizioni**. Non dichiarare un miglioramento di campo: CrUX e RUM richiedono nuove visite.

Con il solo codice sorgente puoi indicare **cause probabili**, ma non affermare che LCP, INP o CLS falliscono. Non confrontare un singolo valore di laboratorio con un p75 di campo come se fossero la stessa misura.

## Soglie (75° percentile)

| Metrica | Misura | Buono | Da migliorare | Scarso |
|---|---|---|---|---|
| LCP | caricamento | ≤ 2,5 s | 2,5-4 s | > 4 s |
| INP | reattività | ≤ 200 ms | 200-500 ms | > 500 ms |
| CLS | stabilità visiva | ≤ 0,1 | 0,1-0,25 | > 0,25 |

## LCP

- L'elemento LCP (di solito immagine o video dell'hero, oppure un grande blocco di testo) è presente nell'**HTML iniziale**, non inserito da JavaScript dopo un fetch lato client.
- Gli dai priorità alta (`fetchpriority="high"` o l'API di priorità della versione installata del framework) e **non** lo carichi in lazy.
- Aggiungi un preload solo se la traccia mostra che la risorsa viene scoperta tardi: preload superflui competono per la banda.
- Immagine nel formato e nella dimensione giusti (AVIF o WebP, `srcset` e `sizes` corretti).
- Tempo di risposta del server sotto controllo (cache, CDN, rendering statico o in streaming dove possibile).
- Font che non bloccano il testo (`font-display: swap` o lo strumento del framework) e preload solo dei font critici.
- CSS e JavaScript bloccanti nel `<head>` ridotti al necessario; script con `defer` o `async`.

## INP

Scomponi l'interazione lenta in ritardo di input, tempo di elaborazione e ritardo di presentazione: le cause sono diverse.
- **Ritardo di input**: task lunghi sul main thread prima del gestore (script di terze parti, hydration, lavoro in background). Spezzali cedendo il main thread tra una parte e l'altra.
- **Elaborazione**: gestori costosi. Fai subito solo il lavoro che produce il feedback visibile e rimanda il resto; rendi economici gli input controllati a ogni tasto.
- **Presentazione**: rendering pesante dopo il gestore. Riduci il DOM coinvolto, evita letture di layout forzate subito dopo una scrittura, virtualizza le liste lunghe o usa `content-visibility: auto`.
- Usa lo strumento di virtualizzazione che il progetto ha già; aggiungerne uno è una decisione da proporre.

## CLS

- Spazio riservato per tutto ciò che arriva dopo: immagini (`width`/`height` o `aspect-ratio`), embed, annunci, banner, contenuti caricati dinamicamente.
- Nessun contenuto inserito sopra quello esistente, salvo in risposta a un'azione dell'utente.
- Font con fallback metricamente compatibile (`size-adjust` e affini, o lo strumento del framework) per evitare lo spostamento allo swap.
- Animazioni con `transform`, non con proprietà che cambiano il layout.
- Individua il nodo che si è spostato **e** la causa con l'attribuzione di campo o con la traccia: l'elemento che si vede saltare spesso non è il colpevole.

## Caricamento e bundle

- Importa direttamente dai moduli invece che dai file barile nei percorsi caricati di frequente, a meno che il bundler del progetto li ottimizzi già (verificalo).
- Import dinamico per componenti pesanti o usati solo in certe condizioni (editor, grafici, mappe, modali rare).
- Script di terze parti (analytics, chat, tracciamento) caricati dopo l'hydration o in idle, salvo requisiti contrari.
- Precarica al passaggio del mouse o al focus ciò che l'utente sta per aprire.
- Le Speculation Rules (prerender della pagina successiva probabile) sono un miglioramento progressivo da misurare: ogni prerender costa quanto un caricamento completo, e analytics ed effetti collaterali partono prima che l'utente navighi. Si attivano solo sui browser Chromium. Non sostituiscono la correzione dell'LCP della pagina corrente.

## Fonti di misura

| Fonte | Uso |
|---|---|
| Traccia del browser (Chrome DevTools MCP o pannello Performance) | diagnosi di un caricamento o di un'interazione |
| CrUX o Search Console | priorità basata sugli utenti reali al p75 |
| Lighthouse CLI o PageSpeed Insights | laboratorio controllato quando non c'è altro |
| RUM del progetto (libreria `web-vitals`) | esperienza reale per route, dispositivo e release |
| `PerformanceObserver` in console | debug di una singola sessione, non dati di campo |

## Report

Per ogni affermazione indica la metrica, la fonte (campo, laboratorio o inferenza dal codice) e le condizioni della misura. "LCP 3,1 s in laboratorio, profilo mobile, cache vuota" è un dato. "La pagina è lenta" non lo è.
