# Taxi Grid World: appunti personali

Note mie sul progetto di Intro to AI (ricerca su grafo con A*). Il README del prof resta `README.md`; questo è solo per me.

## 1. Cosa fa il progetto

Un taxi parte da (0,0) su una griglia 15x15 con muri e terreni a costo diverso. Deve:

1. andare alla stazione rossa (4,4) e fare `PICKUP`
2. portare il passeggero alla stazione verde (0,14) e fare `DROPOFF`

L'obiettivo è farlo col **costo totale minimo**, non col minor numero di mosse.

Costi del terreno: strada `.` = 1, residenziale `r` = 3, traffico `t` = 5, casello `$` = 10, muro `#` = impassabile. Pickup e dropoff costano 1 ciascuno.

## 2. Come farlo partire

Tutti i comandi sono da WSL (Ubuntu).

**1. Attivare il venv** (se non c'è `(.venv_ia)` davanti al prompt):

```bash
source /mnt/c/Users/kokin/Desktop/Prog_Script/Intro-To-IA/.venv_ia/bin/activate
```

**2. Spostarsi nella cartella `projects`**, cioè quella che *contiene* la cartella `taxi`:

```bash
cd /mnt/c/Users/kokin/Desktop/Prog_Script/Intro-To-IA/Tutorati/projects
```

**3. Lanciare il test** (usa `taxi/submission.py`):

```bash
python -m taxi.test
```

**4. (Facoltativo) Giocare a mano** con WASD per muoversi, E per pickup, Q per dropoff:

```bash
python -m taxi.runner
```

Il comando va sempre lanciato da `projects`, non da dentro `taxi`. Altrimenti Python non trova `taxi.submission`.

## 3. Come leggere il risultato

L'output è un dizionario:

```
{'solution': True, 'cost': 97.0, 'steps': 70, 'optimal_solution': True, 'search_time': 0.0013}
```

- `solution`: il taxi ha consegnato il passeggero
- `cost`: costo totale cumulativo (quello che conta)
- `steps`: numero di azioni eseguite
- `optimal_solution`: `True` se il costo è uguale a quello atteso dal test
- `search_time`: secondi medi per una ricerca (10 ripetizioni), circa 1,3 ms

Il `RuntimeWarning` su pygame e AVX2 si può ignorare, non c'entra col codice.

## 4. Risultati

Costo ottimo = **97** = 24 (taxi → passeggero) + 2 (pickup + dropoff) + 71 (passeggero → destinazione). Verificato anche con un Dijkstra a parte.

Nota storica: nella prima versione `test.py` confrontava con **71**, che è solo il costo del secondo tratto, quindi `optimal_solution` usciva `False` anche con la soluzione giusta. Il prof l'ha corretto in `== 97`.

## 5. Come funziona il codice (`submission.py`)

Algoritmo: **A\*** in graph search.

- **Stato**: tupla `(x, y, status, passenger_loc, destination_loc)`, usata come chiave nei dizionari.
- **`g`**: dizionario con il costo migliore trovato finora per ogni stato.
- **`parent`**: per ogni stato, da quale stato e con quale azione ci sono arrivato (serve a ricostruire il piano).
- **`frontier`**: coda di priorità (`heapq`) con tuple `(f, -g, stato)`, dove `f = g + h`. A parità di `f` esce prima lo stato con `g` maggiore.
- **Entry vecchie**: `heapq` non permette di cambiare una priorità, quindi inserisco le copie migliori e salto quelle vecchie quando le estraggo.
- **Goal test all'estrazione**, non alla generazione: solo allora il costo è sicuramente minimo.
- **Piano**: risalgo da goal a start con `parent`, poi `reverse()`. `act()` consuma il piano un'azione alla volta.

### Euristica

Distanza di Manhattan divisa per fase, ignorando muri e costi del terreno:

- passeggero in attesa: taxi → passeggero + passeggero → destinazione + 2 (pickup e dropoff)
- passeggero a bordo: taxi → destinazione + 1 (dropoff)
- consegnato: 0

Perché va bene:

- **Ammissibile**: ogni mossa costa almeno 1, quindi |dx|+|dy| non supera mai il costo vero.
- **Consistente**: una mossa abbassa `h` al massimo di 1, che è ≤ del suo costo.
- **Non usa il percorso ottimo**, come richiede la consegna.

### Perché A\* e non BFS

La BFS minimizza il numero di mosse, ma qui conta il costo: 3 mosse su traffico costano 15, 6 mosse su strada costano 6. A\* (come UCS) tiene conto dei costi, e in più usa l'euristica per esplorare meno stati.

## 6. File del progetto

| File | Cosa è |
| :--- | :--- |
| `taxi/submission.py` | la consegna (inglese, A*) |
| `taxi/submission_ita.py` | stessa soluzione, commenti in italiano, per studiare |
| `taxi/agent.py` | template del prof |
| `taxi/environment.py` | l'ambiente (non toccare) |
| `taxi/test.py` | test del prof (non toccare) |
| `taxi/runner.py` | gioco manuale |

## 7. Problemi già incontrati

- **`python -m taxi.test` non trova `taxi`**: sei nella cartella sbagliata. Fai `cd` in `projects`.
- **Venv non attivo**: manca `(.venv_ia)` davanti al prompt. Rifai il `source` del punto 2.
- **`submission.py` non compare in `git status`**: il `.gitignore` copiato dal prof ignora `projects/taxi/submission.py`. Per salvarlo: `git add -f taxi/submission.py`.
- **Se rinomino `submission.py`**, il test non gira più, perché importa `taxi.submission`.
- **Se scarico di nuovo i file del prof**, attenzione a non sovrascrivere `submission.py` o questo README.