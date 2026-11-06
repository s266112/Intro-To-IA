"""
    COPIA QUESTO CODICE DENTRO `submission.py` (NELLA STESSA CARTELLA DI QUESTO FILE).
    Rimuovi questo commento e aggiungi invece una riga con scritto solo:
        -`name`, `surname`, `student id`
    COMPLETA LE PARTI RICHIESTE. PUOI CAMBIARE QUELLO CHE VUOI, MA:

    - devi mantenere la definizione dei metodi così come sono
    - devi usare un algoritmo di ricerca come quelli visti a lezione per risolvere il task
    - non puoi usare il percorso ottimo come euristica
    - devi descrivere le tue decisioni con commenti qua e là
    - non devi usare solo LLM / agenti per risolvere il task. Se lo fai, lo sapremo.

    La soluzione sarà valutata in base a:

    - il tuo algoritmo trova una soluzione?
    - il tuo algoritmo trova la soluzione ottima (in termini di costo cumulativo)
    - quanto tempo impiega il tuo algoritmo a trovare la soluzione?

    Per ottenere il punteggio massimo è sufficiente trovare la soluzione ottima.
    Coloro che performano meglio in termini di prestazioni otterranno punti aggiuntivi.
"""
class Agent():

  def __init__(self, env): # NON CAMBIARE LA DEFINIZIONE
    self.env = env # questa è un'istanza di TaxiWorld
    self.plan = []
    self.search()

  def act(self): # NON CAMBIARE LA DEFINIZIONE
    """Funzione principale chiamata dal runner per eseguire un'azione."""
    # Si assume che self.search sia già stata chiamata
    if self.plan:
      return self.plan.pop(0)
    return 0 # Fallback

  def search(self): # NON CAMBIARE LA DEFINIZIONE
    """
    QUESTO È IL METODO CHE DEVI IMPLEMENTARE.

    Routine di ricerca principale: costruisce l'albero di ricerca e trova un percorso verso il goal.

    Questo metodo deve popolare self.plan.

    Usando questo metodo dovresti sfruttare le utility dell'ambiente per la ricerca.

    Ti ricordiamo:
        - is_goal(state)
        - get_possible_actions(state)
        - get_action_cost(state, action)
        - get_successor(state, action)
    Puoi leggere i dettagli implementativi direttamente nell'environment.py di questa cartella.

    Nota: le utility assumono già che la forma dello stato sia:

        (taxi_x, taxi_y, passenger_status, passenger_station, destination_station)
    
    passenger_status può essere:

        PASSENGER_WAITING
        PASSENGER_IN_TAXI
        PASSENGER_DELIVERED
    """
    self.plan = []
    pass