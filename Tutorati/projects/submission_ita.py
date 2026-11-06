# Alessio Matessi SM3201657
 
import heapq
 
class Agent():
 
    def __init__(self, env):
        self.env = env
        self.plan = []
        self.search()
 
    def act(self):
        """Restituisce la prossima azione dal piano, una alla volta."""
        if self.plan:
            return self.plan.pop(0) # Prendo la prima azione e la rimuovo
        return 0                    # Piano vuoto. (Non succede se search è corretto)
 
    def heuristic(self, state):
        """Stima del costo che manca al goal: distanza di Manhattan divisa per fase"""
        x, y, status, p_loc, d_loc = state
 
        # Passeggero in attesa: vado dal passeggero, poi alla destinazione
        if status == 0:
            px, py = self.env.stations[p_loc]["pos"]
            dx, dy = self.env.stations[d_loc]["pos"]
            # + 2 perchè pickup e dropoff costano 1 ciascuno
            return (abs(x - px) + abs(y - py) + abs(px - dx) + abs(py - dy)) + 2
 
        # Passeggero a bordo: devo solo arrivare alla destinazione
        if status == 1:
            dx, dy = self.env.stations[d_loc]["pos"]
            # + 1 perchè il dropoff costa 1
            return (abs(x - dx) + abs(y - dy)) + 1
 
        # Passeggero a destinazione: sono già al goal
        return 0
 
    def search(self):
        """Trova un percorso a costo minimo dal taxi al goal (A*) e lo salva in self.plan"""
 
        # 1. Inizializzo il piano e leggo lo stato di partenza
        self.plan = []
        start = self.env.get_state()
 
        # 2. Se il taxi e gia sul goal, non faccio nulla
        if self.env.is_goal(start):
            return
 
        # 3. Struttura di A*
        g = {start: 0}                  # Costo percorso migliore trovato per arrivare a s
        parent = {start: (None, None)}  # Nodo genitore e azione per arrivare a s
 
        # 4. Coda di priorità ordinata per f = g + h crescente
        """ Inserisco f, poi -g, poi lo stato. A parità di f heapq guarda -g, quindi estrae prima lo stato con g più grande (più vicino al goal)"""
        frontier = [(self.heuristic(start), 0, start)]
 
        goal_state = None
 
        # 5. Ciclo principale di A*
        while frontier:
            f, neg_g, state = heapq.heappop(frontier)
            g_cost = -neg_g
 
            # Salto se ho gia trovato un percorso migliore per questo stato
            if g_cost > g.get(state, float('inf')):
                continue
 
            # 6. Test del goal
            """ Lo faccio quando estraggo lo stato dalla coda e non quando lo genero, perchè solo allora sono sicuro che il suo costo è il minimo"""
            if self.env.is_goal(state):
                goal_state = state
                break
 
            # 7. Espansione dello stato corrente
            for action in self.env.get_possible_actions(state):
                cost = self.env.get_action_cost(state, action)
                succ = self.env.get_successor(state, action)
                new_g = g_cost + cost
 
                # Aggiorno solo se ho trovato un costo migliore
                if new_g < g.get(succ, float('inf')):
                    g[succ] = new_g
                    parent[succ] = (state, action)
                    heapq.heappush(frontier, (new_g + self.heuristic(succ), -new_g, succ))
 
        # 8. Se non ho mai raggiunto il goal, lascio il piano vuoto
        if goal_state is None:
            return
 
        # 9. Ricostruisco il piano a partire dal goal
        actions = []
        cur = goal_state
        while parent[cur][0] is not None:
            prev, action = parent[cur]
            actions.append(action)
            cur = prev
        actions.reverse()
        self.plan = actions




# --- SPIEGAZIONE DELLE SCELTE ---

# 1. PERCHE' HO SCELTO A* E NON BFS?
#     Ho scelto A* e non BFS perche i terreni hanno costi diversi: la BFS minimizza il numero di azioni,
#     A* invece tiene conto dei costi di tutti i passi e trova il percorso a costo totale minimo.
#     Inoltre, A* usa un'euristica per guidare la ricerca, e in generale esplora meno stati
#     di una ricerca a costo uniforme (UCS).


# 2. COSA FA L'EURISTICA?
#     L'euristica stima il costo per raggiungere il goal da uno stato dato: calcolo la distanza di Manhattan
#     (senza contare muri o terreni), tra taxi, passeggero e destinazione, più 1 per il pickup e 1 per il dropoff ancora da fare.
#     Ho usato Manhattan perché il taxi si muove solo in 4 direzioni, quindi è il numero minimo di mosse
#     necessarie, e si calcola velocemente.
#     Deve essere ammissibile, cioè non sopravvalutare mai il costo reale, per garantire che A* trovi la soluzione ottima.

# 3. PERCHE' LA STIMA NON SOPRAVVALUTA MAI IL COSTO REALE?
#     Perché la distanza di Manhattan è il numero minimo di mosse per andare da una cella a un'altra, e ogni mossa costa almeno 1 
#     (la strada è il terreno più economico). Quindi il costo reale è sempre maggiore o uguale alla stima.
#     Pickup e dropoff li conto esattamente 1 ciascuno, come costano davvero.


# 4. PERCHE' CONTROLLO IL GOAL ALL'ESTRAZIONE DALLA CODA E NON ALLA GENERAZIONE?
#     Perché, con un'euristica ammissibile e consistente, A* garantisce che il primo stato goal estratto dalla coda sia quello con il costo minimo. 
#     Se controllassi il goal alla generazione, potrei trovare uno stato goal con un costo maggiore di uno che troverei successivamente. 
#     In questo modo, invece, quando estraggo uno stato goal dalla coda, sono sicuro che il suo costo è il
#     minimo possibile, quindi posso fermarmi e ricostruire il piano ottimo.