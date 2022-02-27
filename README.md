# ArgoScuolaNext per Python

Un'implementazione in Python dei servizi restful di ArgoScuolaNext.

Se prediligi Node.js e vuoi documentarti meglio per quanto
riguardo i metodi della libreria,
[ReLoia/ArgoScuolaNext-NodeJS](https://github.com/ReLoia/ArgoScuolaNext-NodeJS) potrebbe fare al caso tuo.

### Disclaimer

Sebbene ad oggi questo progetto sia uno di quelli a cui sono più affezionato, purtroppo questa libreria non
riceve né riceverà più alcun tipo di aggiornamento. L'impiego di questa libreria, inoltre, è contrario ai termini
di servizio della piattaforma ArgoScuolaNext. Questo repository, non aggiornato, rimane tuttavia archiviato
pubblicamente per scopi informativi.

> Il token di autenticazione e i servizi restful invocati mediante esso, possono essere utilizzati solo dall'applicazione "DidUP - Famiglia" della Argo Software SRL per l’erogazione dei propri servizi o da fornitori saas e relative applicazioni appositamente preautorizzate, in conformità alla vigente normativa in maniera di protezione dei dati personali ed alle misure richieste dall’AgID per gli applicativi SaaS delle PA.

## Installazione

Per installare questa libreria, è sufficiente utilizzare pip:

```bash
pip install -U git+https://github.com/hearot/ArgoScuolaNext.git
```

## Importare la libreria

Per importare la libreria, è sufficiente inserire nel codice il seguente preambolo:

```python
import argoscuolanext

...
```

## Login

Per effettuare il login e creare la sessione, è necessario inizializzare la classe
`argoscuolanext.Session` con `schoolCode` (il codice della scuola), `username` e
`password` come parametri.

```python
import argoscuolanext

session = argoscuolanext.Session("schoolCode", "username", "password")
```

## Richiamare un metodo

Le API contemplano numerosi metodi, tra i quali i più importanti sono i seguenti:

- `argomenti`
- `assenze`
- `compiti`
- `docenticlasse`
- `notedisciplinari`
- `oggi`
- `orario`
- `promemoria`
- `votigiornalieri`
- `votiscrutinio`

Per richiamare un metodo è sufficiente trattarlo come un metodo della classe `Session`.

Alcuni metodi ammettono come parametro una data nel formato `yyyy-mm-dd` (o come istanza
della classe `datetime.datetime`). Per esempio, per richiamare il metodo `oggi` nella
data `2019-10-06` è sufficiente il seguente codice:

```python
...

session.oggi("2019-10-06")
```
