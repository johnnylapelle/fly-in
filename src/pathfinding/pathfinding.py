from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue
import heapq


class Pathfinding:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self.heuristic: dict[Zone, int] = {}
        self.reservations: dict[tuple[str, int], int] = {}
        self._dijkstra_search()

    def _dijkstra_search(self) -> None:
        start = self._graph.end
        frontier = PriorityQueue()
        frontier.put(start, 0)
        self.heuristic[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self._graph.get_neighbours(current):
                next_zone = next.get_other(current)
                new_cost = (self.heuristic[current]
                            + self._graph.cost(current))

                if (next_zone not in self.heuristic
                   or new_cost < self.heuristic[next_zone]):
                    self.heuristic[next_zone] = new_cost
                    priority = new_cost
                    frontier.put(next_zone, priority)

    def space_time_a_star(self):
        path: dict[tuple[Zone, int], tuple[str, int] | None] = {}
        cost_so_far: dict[tuple[Zone, int], int] = {}
        open_list = PriorityQueue()
        closed_set: set[tuple[Zone, int]] = set()

        start = self._graph.start
        start_state = (start, 0)

        cost_so_far[start_state] = 0
        path[start_state] = None
        open_list.put((start, 0, 0), priority=self.heuristic[start])

        while not open_list.empty():
            current, turn, g = open_list.get()

            if (current, turn) in closed_set:
                continue
            closed_set.add((current, turn))

            if current == self._graph.end:
                break

            for connection in self._graph.get_neighbours(current):
                next_zone = connection.get_other(current)
                move_cost = self._graph.cost(next_zone)
                arrival_turn = turn + move_cost
                new_cost = g + move_cost

                current_state = (current, turn)
                next_state = (next_zone, arrival_turn)

                if (next_state not in cost_so_far or new_cost < cost_so_far[next_state]):
                    f = new_cost + self.heuristic[next_zone]

                    cost_so_far[next_state] = new_cost
                    open_list.put((next_zone, arrival_turn, new_cost), priority=f)
                    path[next_state] = current_state

        return path, cost_so_far


# 1. Initialise open_list avec (start_zone, turn=0)
# 2. Tant que open_list non vide :
#    a. Prendre le nœud avec le f le plus bas
#    b. Si zone == goal → chemin trouvé, retourner path
#    c. Pour chaque connexion depuis zone :
#       - Calculer le voisin et le coût de déplacement
#       - Calculer le turn d'arrivée (turn + coût)
#       - Vérifier que le voisin est disponible dans reservation table
#       - Vérifier que la connexion est disponible
#       - Si disponible → ajouter à open_list
#    d. Ajouter option "attendre sur place" si zone disponible au turn+1
# 3. Si open_list vide → pas de chemin trouvé

    def is_available(self, name: str, turn: int) -> bool:
        max_capacity = self._graph.get_max_capacity(name)
        current = self.reservations.get((name, turn), 0)
        if current >= max_capacity:
            return False
        return True

    def reserve(self, name: str, turn: int) -> None:
        current = self.reservations.get((name, turn), 0)
        current += 1

