# Alessio Matessi SM3201657

import heapq

class Agent():

    def __init__(self, env):
        self.env = env
        self.plan = []
        self.search()

    def act(self):
        """Return the next action from the plan, one at a time."""
        if self.plan:
            return self.plan.pop(0) # Take the first action and remove it
        return 0                    # Empty plan (should not happen if search is correct)

    def heuristic(self, state):
        """Estimate of the remaining cost to the goal: Manhattan distance, split by phase"""
        x, y, status, p_loc, d_loc = state

        # Passenger waiting: go to the passenger, then to the destination
        if status == 0:
            px, py = self.env.stations[p_loc]["pos"]
            dx, dy = self.env.stations[d_loc]["pos"]
            # + 2 because pickup and dropoff cost 1 each
            return (abs(x - px) + abs(y - py) + abs(px - dx) + abs(py - dy)) + 2

        # Passenger in the taxi: only the trip to the destination is left
        if status == 1:
            dx, dy = self.env.stations[d_loc]["pos"]
            # + 1 because the dropoff costs 1
            return (abs(x - dx) + abs(y - dy)) + 1

        # Passenger delivered: already at the goal
        return 0

    def search(self):
        """Find a minimum-cost path from the taxi to the goal (A*) and store it in self.plan"""

        # 1. Initialize the plan and read the starting state
        self.plan = []
        start = self.env.get_state()

        # 2. If the taxi is already at the goal, do nothing
        if self.env.is_goal(start):
            return

        # 3. A* data structures
        g = {start: 0}                  # Best path cost found so far to reach each state
        parent = {start: (None, None)}  # Parent state and action used to reach each state

        # 4. Priority queue ordered by increasing f = g + h
        """ I insert f, then -g, then the state. On equal f, heapq looks at -g,
        so it pops first the state with the larger g (closer to the goal)."""
        frontier = [(self.heuristic(start), 0, start)]

        goal_state = None

        # 5. Main A* loop
        while frontier:
            f, neg_g, state = heapq.heappop(frontier)
            g_cost = -neg_g

            # Skip if a better path to this state has already been found
            if g_cost > g.get(state, float('inf')):
                continue

            # 6. Goal test
            """ I do it when I pop the state from the queue, not when I generate it,
            because only then am I sure its cost is the minimum"""
            if self.env.is_goal(state):
                goal_state = state
                break

            # 7. Expand the current state
            for action in self.env.get_possible_actions(state):
                cost = self.env.get_action_cost(state, action)
                succ = self.env.get_successor(state, action)
                new_g = g_cost + cost

                # Update only if a better cost has been found
                if new_g < g.get(succ, float('inf')):
                    g[succ] = new_g
                    parent[succ] = (state, action)
                    heapq.heappush(frontier, (new_g + self.heuristic(succ), -new_g, succ))

        # 8. If the goal was never reached, leave the plan empty
        if goal_state is None:
            return

        # 9. Rebuild the plan starting from the goal
        actions = []
        cur = goal_state
        while parent[cur][0] is not None:
            prev, action = parent[cur]
            actions.append(action)
            cur = prev
        actions.reverse()
        self.plan = actions




# --- EXPLANATION OF MY CHOICES ---

# 1. WHY DID I CHOOSE A* AND NOT BFS?
#     I chose A* and not BFS because the terrains have different costs: BFS minimizes the number of actions,
#     while A* takes into account the cost of every step and finds the path with the minimum total cost.
#     Moreover, A* uses a heuristic to guide the search, and in general it explores fewer states
#     than uniform-cost search (UCS).


# 2. WHAT DOES THE HEURISTIC DO?
#     The heuristic estimates the cost to reach the goal from a given state: I compute the Manhattan distance
#     (ignoring walls and terrain costs) between taxi, passenger and destination, plus 1 for the pickup and 1 for the dropoff still to be done.
#     I used Manhattan because the taxi moves only in 4 directions, so it is the minimum number of moves
#     needed, and it is fast to compute.
#     It must be admissible, i.e. it must never overestimate the real cost, to guarantee that A* finds the optimal solution.


# 3. WHY DOES THE ESTIMATE NEVER OVERESTIMATE THE REAL COST?
#     Because the Manhattan distance is the minimum number of moves to go from one cell to another, and every move costs at least 1
#     (road is the cheapest terrain). So the real cost is always greater than or equal to the estimate.
#     I count pickup and dropoff as exactly 1 each, which is what they really cost.


# 4. WHY DO I CHECK THE GOAL WHEN POPPING FROM THE QUEUE AND NOT WHEN GENERATING IT?
#     Because, with an admissible and consistent heuristic, A* guarantees that the first goal state popped from the queue is the one with the minimum cost.
#     If I checked the goal at generation time, I could find a goal state with a higher cost than one I would find later.
#     This way, instead, when I pop a goal state from the queue, I am sure its cost is the minimum possible,
#     so I can stop and rebuild the optimal plan.