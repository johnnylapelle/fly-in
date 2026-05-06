from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue
from ..core.exception import PathfindingError
from .reservation_table import ReservationTable


class Pathfinding:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self.heuristic: dict[Zone, int] = {}
        self._dijkstra_search()
        self.res_table = ReservationTable(self._graph)

    def _dijkstra_search(self) -> None:
        start = self._graph.end
        frontier: PriorityQueue = PriorityQueue()
        frontier.put(start, 0)
        self.heuristic[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self._graph.get_neighbours(current):
                next_zone = next.get_other(current)
                new_cost = (self.heuristic[current]
                            + self._graph.cost(next_zone))

                if (next_zone not in self.heuristic
                   or new_cost < self.heuristic[next_zone]):
                    self.heuristic[next_zone] = new_cost
                    priority = new_cost
                    frontier.put(next_zone, priority)

    def space_time_a_star(self) -> list[tuple[Zone, int] | None]:

        path: dict[tuple[Zone, int], tuple[Zone, int] | None] = {}
        cost_so_far: dict[tuple[Zone, int], int] = {}
        open_list: PriorityQueue = PriorityQueue()
        closed_set: set[tuple[Zone, int]] = set()

        start = self._graph.start
        goal = self._graph.end
        start_state = (start, 0)

        cost_so_far[start_state] = 0
        path[start_state] = None
        open_list.put((start, 0, 0), priority=self.heuristic[start])

        while not open_list.empty():
            current, turn, g = open_list.get()

            if (current, turn) in closed_set:
                continue
            closed_set.add((current, turn))

            current_state = (current, turn)

            if current == goal:
                break

            for connection in self._graph.get_neighbours(current):
                next_zone = connection.get_other(current)
                move_cost = self._graph.cost(next_zone)
                arrival_turn = turn + move_cost
                new_cost = g + move_cost

                next_state = (next_zone, arrival_turn)

                if not self.res_table.is_available(connection.key, turn):
                    continue
                if not self.res_table.is_available(
                 next_zone.name, arrival_turn):
                    continue

                if (next_state not in cost_so_far
                   or new_cost < cost_so_far[next_state]):
                    f = new_cost + self.heuristic[next_zone]

                    cost_so_far[next_state] = new_cost
                    open_list.put(
                        (next_zone, arrival_turn, new_cost), priority=f)
                    path[next_state] = current_state

            if (current.is_start
               or self.res_table.is_available(current.name, turn + 1)):
                f = g + 1 + self.heuristic[current]
                open_list.put(
                    (current, turn + 1, g + 1), priority=f)
                path[(current, turn + 1)] = (current, turn)

        correct_path = self.reconstruct_path(path, turn, goal)
        return correct_path

    def reconstruct_path(
            self,
            path: dict[tuple[Zone, int], tuple[Zone, int] | None],
            turn: int,
            goal: Zone) -> list[tuple[Zone, int] | None]:

        correct_path: list[tuple[Zone, int] | None] = []
        current: tuple[Zone, int] | None = (goal, turn)

        if (goal, turn) not in path:
            raise PathfindingError("No path was found.")

        while current is not None:
            correct_path.append(current)
            current = path[current]

        correct_path.reverse()
        return correct_path

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
