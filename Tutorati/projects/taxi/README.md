# Taxi Grid World — Progetto Algoritmi di Ricerca

Benvenuto nell'assegnazione **Taxi Grid World**! In questo progetto implementerai algoritmi di ricerca (come Uninformed Search e $A^*$ Search) con diverse euristiche per trovare il **percorso a costo minimo** per un tassista. Il tuo obiettivo è navigare da una posizione iniziale per prelevare un passeggero e consegnarlo alla destinazione target con costo di percorso minimo.

---

## Panoramica e definizione del problema

L'ambiente rappresenta una mappa cittadina a griglia contenente ostacoli (muri), tipi di terreno con costi diversi, un punto di prelievo del passeggero e un punto di consegna finale.

Il tuo compito è diviso in due fasi:

1. **Fase di prelievo:** Guida dalla posizione iniziale del taxi fino alla stazione del passeggero ed esegui l'azione `PICKUP`.
2. **Fase di consegna:** Trasporta il passeggero dalla posizione di prelievo alla stazione di destinazione ed esegui l'azione `DROPOFF`.

L'obiettivo è raggiunto quando il passeggero è consegnato con successo e il taxi si trova alla destinazione finale.

---

## Rappresentazione dello stato

Per applicare algoritmi di ricerca su grafo come BFS, Uniform Cost Search (UCS) o $A^*$, devi tenere traccia delle transizioni di stato. Lo stato in `TaxiWorld` è rappresentato come una 5-tupla:

$$\text{State} = (x, y, \text{status}, \text{passenger\_loc}, \text{destination\_loc})$$

- **$x, y$**: coordinate attuali del taxi sulla griglia (indicizzate da 0).
- **$\text{status}$**: stato attuale del passeggero:
  - `0`: `PASSENGER_WAITING` (in attesa al punto di prelievo)
  - `1`: `PASSENGER_IN_TAXI` (in transito)
  - `2`: `PASSENGER_DELIVERED` (alla destinazione)
- **$\text{passenger\_loc}$**: indice della stazione di prelievo del passeggero (`0` = Red Station).
- **$\text{destination\_loc}$**: indice della stazione di destinazione (`1` = Green Station).

---

## Azioni e costi di movimento

Lo spazio delle azioni è composto da 6 azioni discrete:

| ID azione | Nome azione | Descrizione | Costo base |
| :---: | :---: | :--- | :---: |
| `0` | `UP` | Muovi in su di 1 cella | Dipendente dal terreno |
| `1` | `DOWN` | Muovi in giù di 1 cella | Dipendente dal terreno |
| `2` | `LEFT` | Muovi a sinistra di 1 cella | Dipendente dal terreno |
| `3` | `RIGHT` | Muovi a destra di 1 cella | Dipendente dal terreno |
| `4` | `PICKUP` | Preleva il passeggero alla stazione | `1` |
| `5` | `DROPOFF` | Consegna il passeggero alla destinazione | `1` |

### Costi del terreno

Celle diverse della griglia comportano costi di attraversamento diversi:

| Simbolo | Tipo di terreno | Colore nel render | Costo (impatto su $g(n)$) |
| :---: | :--- | :--- | :---: |
| `.` | Strada | Grigio chiaro | `1` |
| `r` | Area residenziale | Verde chiaro | `3` |
| `t` | Zona di traffico | Arancione chiaro | `5` |
| `$` | Casello | Viola chiaro | `10` |
| `#` | Muro | Grigio scuro | Impassabile |

> **Nota:** il reward di passo restituito da `env.step(action)` è il costo dell'azione con segno negativo ($R = -c$). Una mossa illegale comporta una penalità di costo $5$ e lascia lo stato invariato.

---

## Metodi principali dell'ambiente per la ricerca

Puoi interfacciarti con l'ambiente direttamente tramite metodi di supporto pensati appositamente per gli algoritmi di ricerca, senza modificare lo stato live:

### Metodi per stato e azioni

- `env.get_state()`: restituisce la tupla dello stato corrente.
- `env.is_goal(state=None)`: verifica se lo stato dato (o quello corrente) soddisfa la condizione di goal.
- `env.get_possible_actions(state=None)`: restituisce una lista di azioni legali disponibili dallo stato specificato.
- `env.get_action_cost(state, action)`: restituisce il costo di transizione dell'esecuzione di `action` da `state`. Restituisce `inf` per azioni illegali.
- `env.get_successor(state, action)`: restituisce la tupla del **prossimo stato** risultante dopo aver eseguito `action` da `state` ( **non** altera l'ambiente reale).

### Posizioni delle stazioni

Puoi accedere alle coordinate delle stazioni tramite `env.stations`:

- **Red Station (Prelievo):** `env.stations[0]["pos"]` $\rightarrow (4, 4)$
- **Green Station (Consegna):** `env.stations[1]["pos"]` $\rightarrow (0, 14)$

---

## Esempio

Ecco un semplice esempio che mostra come "giocare" al gioco usando `WASD` e `EQ` come tasti per i movimenti e per pickup e dropoff (guarda direttamente il codice in `taxi\runner.py` per ulteriori riferimenti).

```bash
cd projects
py -m taxi.runner