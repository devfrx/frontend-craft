# Accessibilità — WCAG 2.2 AA

Obiettivo di default: **WCAG 2.2 livello AA**. Per obblighi normativi specifici (per esempio in ambito UE) il riferimento è la skill `compliance-docs`, se disponibile: qui si tratta di come costruire e verificare, non di cosa impone una legge.

## Workflow basato su evidenza

Con una pagina renderizzabile:
1. Esegui un audit automatico dell'accessibilità: Lighthouse o axe, tramite Chrome DevTools MCP se disponibile, altrimenti da riga di comando se già presenti nel progetto.
2. Usa i nodi che falliscono per localizzare il componente o il template, invece di cercare pattern generici in tutto il repo.
3. Ispeziona l'albero di accessibilità renderizzato: nomi, ruoli, stati, landmark, struttura dei titoli.
4. Percorri il flusso interessato **solo con la tastiera**.
5. Correggi nel sorgente, poi ripeti lo stesso audit e lo stesso percorso.

Senza pagina renderizzabile, lavora sul codice e dichiara che la verifica runtime manca.

Gli strumenti automatici trovano solo una parte delle barriere. **Un punteggio di 100 non è conformità WCAG**, e un punteggio basso non sostituisce i findings puntuali.

## Soglie, verificate su W3C

**Contrasto** (misuralo con `scripts/contrasto.py`):

| Contenuto | AA | AAA |
|---|---|---|
| Testo normale | 4,5:1 (1.4.3) | 7:1 (1.4.6) |
| Testo grande: almeno **24px**, oppure almeno **18,67px in grassetto** | 3:1 | 4,5:1 |
| Componenti d'interfaccia, stati, indicatore di focus, grafica necessaria alla comprensione | 3:1 (1.4.11) | — |

WCAG definisce il testo grande in *punti* (18pt, oppure 14pt in grassetto) e in CSS 1pt equivale a 4/3 px. Tabelle che parlano di "18px / 14px grassetto" sono sbagliate e fanno passare testo che non passa. Il rapporto non si arrotonda: 4,49:1 non supera 4,5:1. Il testo del placeholder è testo e segue le stesse soglie.

**Dimensione dei target** (2.5.8, AA): almeno 24×24px CSS. Eccezioni: target più piccoli distanziati in modo che un cerchio di 24px centrato su ciascuno non tocchi gli altri; un controllo equivalente altrove nella pagina; link dentro un testo; dimensione decisa dal browser; dimensione essenziale. Il valore di 44×44px è una raccomandazione per interfacce touch, non il minimo AA. Sotto 24px è P1; tra 24 e 44 su un'interfaccia touch è P2 o P3.

## Criteri nuovi in WCAG 2.2

- **2.4.11 Focus non oscurato (AA)**: l'elemento con il focus non deve essere nascosto del tutto da contenuti sticky o sovrapposti.
- **2.5.7 Movimenti di trascinamento (AA)**: ogni azione che richiede un trascinamento ha un'alternativa con un solo puntatore (bottoni, input).
- **2.5.8 Dimensione minima dei target (AA)**: vedi sopra.
- **3.2.6 Aiuto coerente (A)**: se un meccanismo di aiuto si ripete su più pagine, appare nello stesso ordine relativo.
- **3.3.7 Inserimento ridondante (A)**: non far reinserire dati già forniti nella stessa sessione (compilali o rendili selezionabili), salvo sicurezza o dati scaduti.
- **3.3.8 Autenticazione accessibile (AA)**: niente test cognitivi (ricordare, trascrivere, risolvere enigmi) senza alternativa. Consentire incolla e autocompilazione nei campi password basta a soddisfarlo; passkey, SSO e link via email sono alternative valide.
- **4.1.1 Parsing** è stato rimosso in WCAG 2.2: non segnalarlo come violazione.

## Criteri AA da ricordare più spesso

- **1.1.1** alternative testuali; **1.3.1** struttura e relazioni nel markup (titoli, liste, tabelle, label).
- **1.3.4** nessun blocco dell'orientamento; **1.3.5** `autocomplete` corretto sui campi che raccolgono dati dell'utente.
- **1.4.1** mai il solo colore per trasmettere informazione: aggiungi testo, icona o forma.
- **1.4.4 / 1.4.10** testo ingrandibile al 200%, layout che si ridispone a 320px CSS senza scroll in due direzioni.
- **1.4.12** spaziatura del testo modificabile senza perdita di contenuto; **1.4.13** contenuti che compaiono al passaggio o al focus: chiudibili, esplorabili col puntatore, persistenti.
- **2.1.1 / 2.1.2** tutto operabile da tastiera, nessuna trappola.
- **2.2.2** movimento automatico oltre 5 secondi: pausa, stop o nascondi.
- **2.3.1** non più di tre lampeggi al secondo.
- **2.4.3 / 2.4.7** ordine del focus logico e focus visibile.
- **2.5.3** il nome accessibile contiene il testo visibile dell'etichetta.
- **3.1.1** `lang` sulla pagina (e sulle parti in altra lingua); **3.3.1 / 3.3.3** errori identificati, con suggerimento di correzione.
- **4.1.2** nome, ruolo e valore esposti; **4.1.3** messaggi di stato annunciati senza spostare il focus (`role="status"` o `aria-live="polite"`).

## Pattern

- **Nativo prima di ARIA.** `<button>`, `<a href>`, `<input>`, `<select>`, `<dialog>`, `<details>` danno gratis focus, attivazione e semantica.
- Se devi usare un elemento non nativo come controllo: `role`, `tabindex="0"`, attivazione con Enter e Spazio, stato esposto (`aria-pressed`, `aria-expanded`…). **Mai** aggiungere gestori da tastiera a un `<button>` nativo: Enter e Spazio generano già il clic e l'azione partirebbe due volte.
- Widget composti (tab, combobox, menu, tree, listbox): usa le primitive accessibili del progetto (Radix, Base UI, React Aria, Angular Aria, Angular CDK, Headless UI…) prima di scriverne di nuove. Se devi scriverle, segui i pattern WAI-ARIA Authoring Practices.
- Dialog, sheet e drawer hanno sempre un titolo, visivamente nascosto se necessario.
- Classe per nascondere visivamente mantenendo il testo per gli screen reader: usa quella del progetto (`sr-only` o equivalente) prima di crearne una nuova.
- Errori dei form: `aria-invalid="true"` sul campo, messaggio collegato con `aria-describedby`, focus sul primo errore all'invio, annuncio con regione live se la validazione è asincrona.

## Reduced motion

Ridurre il movimento significa **togliere o ridurre il movimento spaziale** (parallasse, zoom, grandi scorrimenti, animazioni automatiche) e **mantenere** le transizioni di opacità, colore e stato che confermano un'azione. Non significa spegnere tutto.

Un azzeramento globale delle durate (per esempio a `0.01ms` con `!important`) può restare come rete di sicurezza, ma non sostituisce un'alternativa progettata per ogni componente. Se cancella un feedback che conferma un'azione, è un difetto. Le animazioni decorative in loop si fermano sotto `prefers-reduced-motion` e quando non sono visibili.

## Verifica manuale

- Tastiera: Tab per tutta la pagina, attivazione con Enter e Spazio, Esc sulle sovrapposizioni.
- Screen reader: VoiceOver (macOS/iOS), NVDA (Windows), TalkBack (Android), sul flusso principale.
- Zoom al 200% e ridisposizione a 320px CSS.
- Colori forzati (temi a contrasto elevato di Windows; media query `forced-colors`).
- `prefers-reduced-motion: reduce` attivo.
- Target: nessun controllo sotto 24×24px senza un'eccezione applicabile.

## Severità

Barriera che impedisce di completare un compito a una categoria di utenti: **P0**. Altra violazione AA: **P1**. Violazione AAA o miglioramento oltre AA: P2 o P3, secondo l'impatto.
