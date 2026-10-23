# Fonti, scelte e limiti

Documento per chi mantiene la skill, non da caricare durante il lavoro. Tutto il contenuto è riscritto in italiano: dalle fonti si riprendono idee, soglie e fatti tecnici, non testo.

## Provenienza (fonti primarie lette il 29/09/2026)

| Fonte | Repo @ commit | Licenza | Cosa è stato preso |
|---|---|---|---|
| `frontend-design` (Anthropic) | anthropics/skills @ 8a1541c (28/09/2026) | Apache-2.0 | Radicamento nel soggetto, piano in due passate, default ricorrenti, tipografia, motion orchestrato, moderazione, scrittura nell'interfaccia |
| `webapp-testing` (Anthropic) | anthropics/skills @ 8a1541c | LICENSE.txt della skill | Ricognizione prima dell'azione, raccolta dei log di console. Scartati `with_server.py` e `networkidle` |
| `web-design-guidelines` + Web Interface Guidelines (Vercel) | vercel-labs/agent-skills @ 063bee9; vercel-labs/web-interface-guidelines @ e3d624b (17/08/2026) | MIT (guidelines) | Checklist di interazione, form, focus, contenuti, immagini, tema, i18n, hydration; segnali da cercare nel codice; formato `file:riga` |
| `vercel-react-best-practices` (Vercel) | vercel-labs/agent-skills @ 063bee9 | MIT | Le 8 categorie ordinate per impatto e le regole ad alto impatto, riformulate come principi |
| `next-best-practices` (Vercel) | vercel-labs/next-skills @ c522619 (16/09/2026); vercel/next.js canary @ 63bb9d6 (29/09/2026) | — | Solo il fatto che è stata ritirata e dove sta ora la conoscenza: `next/dist/docs/` e `AGENTS.md` generato |
| `angular-developer` (team Angular) | angular/skills @ 26881df (28/09/2026) | MIT (frontmatter) | Controllo della versione, coerenza con la strategia di form esistente, `ng build` obbligatorio, `effect` non per derivare stato. Letto solo SKILL.md |
| `shadcn` (shadcn) | shadcn-ui/ui @ db2db46 (28/09/2026) | MIT | Principi generalizzati a ogni design system; opzioni `--dry-run` / `--diff` della CLI (verificate in `cli.md`) |
| `figma-design-to-code` (Figma; il report la chiamava `figma-implement-design`) | figma/mcp-server-guide @ 38308b7 (25/09/2026) | nessuna licenza trovata nel repo | Solo principi riformulati: screenshot come target, prototipo da tradurre, riuso di Code Connect, asset esatti, verifica nello scope |
| `accessibility`, `core-web-vitals` (Addy Osmani) | addyosmani/web-quality-skills @ afa8da9 (24/08/2026) | MIT | Workflow basato su evidenza, criteri nuovi di WCAG 2.2, misura prima di ottimizzare, niente affermazioni sul campo senza dati |
| `vue-best-practices` (vuejs-ai) | vuejs-ai/skills @ c9d355f (26/03/2026) | MIT | Fonte unica di verità, flusso esplicito, criteri oggettivi per spezzare i componenti, funzioni opzionali solo se richieste. Letto solo SKILL.md |
| `impeccable` (Paul Bakaus) | pbakaus/impeccable @ 114ea1d (28/09/2026) | Apache-2.0 | Il brief vince, rifinire preserva e ridisegnare sostituisce, modalità della superficie, passate limitate, pavimento di qualità e superfici del browser, classificazione della deriva, euristiche, severità P0-P3, personas, timing del motion, reduced motion |
| `agent-browser` (Vercel Labs) | vercel-labs/agent-browser @ d01253d (22/09/2026) | non verificata | Nessun contenuto: solo l'indicazione di leggere la guida servita dalla CLI se lo strumento è installato |

Altre verifiche su fonti primarie: WCAG (definizione di testo grande, W3C Understanding 1.4.3), documentazione sorgente di Playwright (`networkidle` e `waitForTimeout` sconsigliati, `webServer`, opzioni di `emulateMedia`), CHANGELOG di React (`<Activity>` e `useEffectEvent` in 19.2.0), documentazione di Next.js su canary (`priority` → `preload`, `middleware` → `proxy` in 16.0, API di richiesta asincrone), tarball npm di `next@16.3.7` (contiene `dist/docs/`).

Versioni correnti al 29/09/2026 (registry npm): react 19.3.0, next 16.3.7, tailwindcss 4.3.3, @angular/core 22.2.0, vue 3.5.43, @playwright/test 1.63.0, shadcn 4.21.0.

## Divergenze tra le fonti e come sono state risolte

| Tema | Posizioni | Scelta |
|---|---|---|
| Maiuscole di titoli e bottoni | Vercel: Title Case. Anthropic: sentence case | Convenzione del progetto; di default sentence case; in italiano sempre sentence case |
| Gestori da tastiera | Vercel: su ogni elemento interattivo. Addy: sui nativi causano doppia attivazione | Solo su elementi non nativi con `role` |
| Reduced motion | Addy: azzeramento globale delle durate. Impeccable: alternativa progettata che preserva il feedback | Alternativa per componente; l'azzeramento globale è solo una rete di sicurezza |
| Proprietà animabili | Vercel: solo `transform` e `opacity`. Impeccable: anche blur, maschere e ombre | `transform` e `opacity` di default; le altre solo su regioni limitate e misurate |
| Dimensione dei target | Impeccable: 44×44. WCAG 2.5.8: 24×24 | 24×24 è il minimo AA; 44×44 raccomandato per il touch |
| Testo grande | Addy: 18px / 14px grassetto. WCAG: 18pt / 14pt | 24px / 18,67px grassetto (1pt CSS = 4/3 px) |
| Priorità dell'immagine LCP | Vercel e Addy: `priority` di `next/image` | Deprecata in Next 16 (`preload`): la skill rimanda alla doc della versione installata |
| Attesa nei test | Anthropic: `networkidle` è critico | Playwright lo sconsiglia: asserzioni web-first |
| Eyebrow sopra i titoli | Impeccable: vietato sempre. Anthropic: default da evitare, ma il brief vince | Il brief e il progetto vincono; di default si evita |
| Ordine dei blocchi SFC | vuejs-ai: script, template, style | Ordine già usato nel progetto |
| Librerie suggerite (SWR, nuqs, virtua, better-all) | Vercel le raccomanda | Si usa ciò che il progetto ha; una nuova dipendenza si propone |
| `autocomplete` | Vercel: `off` sui campi non di autenticazione | WCAG 1.3.5 richiede token corretti sui dati personali; `off` solo dove l'autocompilazione è sbagliata |
| Critica con sotto-agenti | Impeccable: due sotto-agenti obbligatori | Due passate indipendenti se disponibili, altrimenti giudizio scritto prima della checklist, dichiarandolo |
| Contesto shadcn | shadcn: `npx shadcn@latest info` a ogni attivazione | Si leggono `components.json` e i file; la CLI solo esplicitamente, a versione fissata |

## Correzioni al report di partenza

- `next-best-practices` non è più una skill: la conoscenza di Next.js arriva con il pacchetto (`next/dist/docs/`, Next 16.3+).
- `figma-implement-design` non esiste più nel repo di Figma: al suo posto c'è `figma-design-to-code`.
- La tabella del contrasto di Addy definisce male il testo grande; `webapp-testing` raccomanda un'attesa che Playwright sconsiglia; `with_server.py` usa ancora `shell=True` su main.

## Escluso, e perché

- **Motion AI Kit**: SKILL.md non accessibile e funzioni principali a pagamento. Le regole di motion vengono da Anthropic, Impeccable e Vercel.
- **`web-artifacts-builder`**: serve solo agli artifact di Claude.ai e fissa Tailwind 3.4.1.
- **`ui-ux-pro-max`, `design-taste-frontend`**, fork e copie: esclusi come nel report (script eseguiti a ogni uso o fonte primaria non letta).
- **Skill Svelte, TypeScript e CSS**: nessuna fonte ufficiale verificata. La skill non ha un reference Svelte; i principi generali valgono comunque.

## Non letto (limiti di questa sintesi)

`vercel-composition-patterns`; i reference di Angular e Vue oltre ai loro SKILL.md; molti reference di Impeccable (`optimize`, `adapt`, `harden` nel dettaglio, `live`, `document`); i file di regole di shadcn oltre a SKILL.md e `cli.md`. Possono contenere indicazioni utili non incluse qui.

## Come aggiornare

Riclona i repo della tabella e confronta i file usati con i commit indicati:
`skills/frontend-design/SKILL.md`, `command.md` delle Web Interface Guidelines, `skills/react-best-practices/SKILL.md`, `skills/accessibility/SKILL.md` e `skills/core-web-vitals/SKILL.md` di Addy, `skill/SKILL.src.md` e `skill/reference/{craft-floor,critique,audit,polish,animate}.md` di Impeccable, `skills/shadcn/SKILL.md` e `cli.md`, lo SKILL.md di Figma per l'implementazione del design, `angular-developer/SKILL.md`, `skills/vue-best-practices/SKILL.md`. Riverifica sulle fonti primarie ogni fatto versionato prima di cambiarlo.
