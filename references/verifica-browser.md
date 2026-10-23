# Verifica nel browser

## Scegli lo strumento disponibile, senza installare di default

In ordine di preferenza:
1. **Test E2E del progetto** (Playwright, Cypress…): eseguili ed estendili nello stesso stile.
2. **Strumenti di browser già presenti nell'ambiente** (Chrome DevTools MCP, estensione browser dell'agente o altro strumento di automazione collegato): ispezione interattiva, screenshot, console, albero di accessibilità, tracce di performance.
3. **`agent-browser`** se è già installato. In quel caso leggi prima la guida servita dalla CLI (`agent-browser skills get core`), che corrisponde alla versione installata, invece di indovinare i comandi.
4. **Nessuno strumento**: dichiaralo e fornisci all'utente i passi manuali per verificare.

Installare Playwright, browser o binari nativi è una modifica all'ambiente: chiedi prima.

## Server di sviluppo

- Avvialo con lo script del progetto (`npm run dev` o equivalente) in background, annota come fermarlo e fermalo prima della consegna, salvo che l'utente voglia tenerlo attivo.
- Con Playwright Test usa l'opzione `webServer` della configurazione (con `reuseExistingServer` fuori dalla CI) invece di helper che lanciano comandi di shell.
- Non costruire comandi di shell concatenando input non fidati.
- Se la porta è già occupata, verifica che risponda l'applicazione giusta: un server estraneo produce verifiche false.

## Playwright scritto bene

- **Locator semantici**: `getByRole`, `getByLabel`, `getByText`, `getByTestId` se il progetto usa test id. Evita selettori CSS fragili legati allo stile.
- **Asserzioni web-first** che attendono da sole: `await expect(locator).toBeVisible()`, `toHaveText`, `toHaveURL`.
- **Non usare `networkidle`**: la documentazione di Playwright lo sconsiglia per i test e indica di affidarsi alle asserzioni. **Non usare `waitForTimeout`**: le attese a tempo sono intrinsecamente instabili.
- **Ricognizione, poi azione**: carica la pagina, attendi un elemento significativo con un'asserzione, fai uno screenshot o leggi l'albero di accessibilità, individua i locator dal render reale e solo allora agisci.
- Raccogli errori di console e richieste fallite durante la navigazione: sono findings.
- Browser headless, chiuso al termine.
- Uno script usa e getta per un controllo va in una cartella temporanea, non nel repo. Un test per un flusso nuovo va nel repo solo se il progetto ha una cultura di test E2E.

## Passata di ispezione raggruppata

Una sola passata che copre tutto, poi le correzioni in blocco, poi al massimo una passata di conferma:
- **Viewport**: desktop (circa 1440px) e mobile (circa 390px) nella stessa passata.
- **Stati**: caricamento, vuoto, errore, successo, disabilitato, testo lungo.
- **Tastiera**: percorso completo dell'azione principale, focus visibile, niente focus coperto da elementi sticky.
- **Preferenze** emulate con `page.emulateMedia`: `reducedMotion: 'reduce'`, `colorScheme: 'dark'` se il tema scuro è supportato, `forcedColors: 'active'` per i colori forzati.
- **Contrasto**: leggi i colori calcolati con `getComputedStyle` e misurali con `scripts/contrasto.py`. Su sfondi con gradiente o immagine lo script non basta: segnala il punto come da verificare a vista, nel caso peggiore.
- **Accessibilità automatica**: audit axe o Lighthouse sulla pagina renderizzata (vedi `accessibilita.md`).

Guarda davvero gli screenshot che produci: un'immagine rivela in un secondo ciò che il codice nasconde. Ma resta dentro le passate previste.

## Riportare l'evidenza

Per ogni verifica indica cosa l'ha prodotta e cosa resta scoperto:
- viewport emulato, tocco sintetizzato, motore di rendering, dispositivo fisico;
- ciò che non è stato provato (per esempio gesti touch reali, Safari, screen reader).

"Layout verificato a 390px in Chromium emulato; gesti touch reali e VoiceOver non provati" è un'informazione utile. "Funziona su mobile" non lo è.
