from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue


class Pathfinding:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._cost_so_far: dict[Zone, int] = {}
        self.reservations: dict[tuple[str, int], int] = {}

        self._dijkstra_search()

    def _dijkstra_search(self) -> None:
        start = self._graph.end
        frontier = PriorityQueue()
        frontier.put(start, 0)
        self._cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self._graph.get_neighbours(current):
                next_zone = next.get_other(current)
                new_cost = (self._cost_so_far[current]
                            + self._graph.cost(current))

                if (next_zone not in self._cost_so_far
                   or new_cost < self._cost_so_far[next_zone]):
                    self._cost_so_far[next_zone] = new_cost
                    priority = new_cost
                    frontier.put(next_zone, priority)

    def is_available(self, name: str, turn: int) -> bool:
        max_capacity = self._graph.get_max_capacity(name)
        if self.reservations[(name, turn)] >= max_capacity:
            return False
        return True

    def reserve(self, name: str, turn: int) -> None:
        self.reservations[(name, turn)] += 1

