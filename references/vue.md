# Vue 3 e Nuxt

## Orientamento specifico

- Versione di Vue, eventuale Nuxt, Pinia, Vue Router, libreria di componenti, `vue-tsc` nella CI.
- **Stile di API già in uso**: Composition API con `<script setup lang="ts">` è il default per il codice nuovo *se il progetto lo usa già o è nuovo*. In un progetto in Options API o JSX si continua in quello stile: migrare è un task a sé, da proporre.
- **Ordine dei blocchi SFC**: quello già usato nel progetto. La guida di stile di Vue chiede coerenza, non un ordine specifico.

## Principi

- **Una sola fonte di verità**: stato minimo in `ref` o `reactive`, tutto il resto derivato con `computed`. I watcher servono agli effetti collaterali, non a copiare stato.
- **Flusso esplicito**: prop verso il basso, eventi verso l'alto. `v-model` solo per veri contratti bidirezionali. `provide`/`inject` solo per contesto profondo, tipizzato con `InjectionKey`.
- **Contratti tipizzati** con `defineProps`, `defineEmits`, `defineModel`.
- **Composable** (`useQualcosa()`) per logica riusata, con stato o con effetti collaterali, con API piccole e tipizzate. La logica di funzionalità sta fuori dai componenti di presentazione.
- **Template dichiarativi**: diramazioni e derivazioni nello script, non in espressioni complesse nel template.

## Quando spezzare un componente

Prima di una funzionalità non banale, prepara una mappa breve: ogni componente con la sua responsabilità in una frase e il suo contratto di prop ed eventi.

Spezza se vale **almeno una** di queste condizioni:
- il componente orchestra stato *e* contiene markup di presentazione per più sezioni;
- ha tre o più sezioni d'interfaccia distinte (per esempio form, filtri, lista, footer);
- un blocco del template si ripete o diventerà riutilizzabile.

Root e viste di route restano sottili: layout, collegamento dei provider, composizione delle funzionalità.

## Funzionalità opzionali, solo se richieste

Slot, attributi passanti, `<KeepAlive>`, `<Teleport>` (overlay), `<Suspense>`, `<Transition>` / `<TransitionGroup>`: si introducono quando il requisito c'è, non per previdenza.

## Sicurezza e insidie

- `v-html` solo con contenuto fidato e sanificato: è una porta per XSS.
- `v-for` con `:key` stabile (un id, non l'indice); mai `v-if` e `v-for` sullo stesso elemento.
- Destrutturare uno store Pinia rompe la reattività: usa `storeToRefs()` per stato e getter; le azioni si destrutturano direttamente.
- Con SSR/Nuxt: niente accesso a `window` o `document` fuori da `onMounted` o dalle guardie client del framework.

## Verifica

`vue-tsc --noEmit` o il typecheck del progetto, lint, test con il framework esistente (Vitest con Vue Test Utils o Testing Library). Nei test di componente verifica il comportamento dall'esterno (prop, eventi, DOM), non l'implementazione, e non affidarti ai soli snapshot.
