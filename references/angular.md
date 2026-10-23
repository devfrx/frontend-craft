# Angular

Se nell'ambiente è installata la skill ufficiale del team Angular (`angular-developer`), per le API del framework segui quella: è mantenuta con il framework. Qui restano le regole di coerenza e verifica.

## Orientamento specifico

- **Versione esatta** di `@angular/core` (package.json, `ng version`). Le best practice e le funzioni disponibili cambiano molto tra le versioni: non proporre API che la versione installata non ha.
- Configurazione degli schematic in `angular.json`: `ng generate` la rispetta, quindi genera con la CLI per restare coerente con naming e struttura.
- Rilevamento dei cambiamenti (zone.js o zoneless), strategia `OnPush`, SSR/hydration, libreria di componenti (Angular Material, CDK, altro).

## Coerenza prima della modernità

- **Form**: per form esistenti si usa la strategia già in uso nell'applicazione (reactive o template-driven). Per form nuovi su Angular 22 o successivo il team Angular raccomanda i Signal Forms; su versioni precedenti, lo stesso approccio dei form esistenti.
- **Naming dei file**: quello già presente nel progetto. La guida di stile dalla v20 ha cambiato le convenzioni, ma un progetto esistente non va rinominato di straforo.
- Le API moderne (signal, control flow `@if` / `@for` con `track` / `@switch`, `input()` / `output()` / `model()`, `inject()`, componenti standalone di default) si usano dove il progetto le usa o nel codice nuovo della versione che le supporta. Mescolare i due stili nello stesso componente no.

## Principi

- Stato con `signal` e `computed`; stato dipendente e scrivibile con `linkedSignal`; dati asincroni con `resource` / `httpResource` dove la versione li offre.
- `effect` solo per effetti collaterali (log, integrazione con DOM o librerie esterne, `afterRenderEffect`), **mai** per derivare stato.
- `standalone: true` è ridondante nelle versioni in cui è il default: non aggiungerlo.
- Pipe nei template; fuori dai template, funzioni pure invece di iniettare una pipe per chiamarne `transform()`.
- Widget accessibili (accordion, listbox, combobox, menu, tab, toolbar, tree, grid) con Angular Aria o CDK prima di scrivere ARIA a mano.

## Verifica

Dopo ogni modifica esegui `ng build` (o lo script di build del progetto) e correggi gli errori prima di proseguire, poi i test con il runner del progetto. Il team Angular considera questo passo obbligatorio, perché gli errori di template e di tipo emergono solo in compilazione.
