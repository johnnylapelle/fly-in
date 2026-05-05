from typing import Optional

from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue


class Pathfinding:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self.heuristic: dict[str, int] = {}

    def dijkstra_search(self, start: Zone, goal: Zone):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: dict[Zone, Optional[Zone]] = {}
        cost_so_far: dict[Zone, int] = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self._graph.get_neighbours(current):
                next_zone = next.get_other(current)
                new_cost = cost_so_far[current] + self._graph.cost(current)
                if next_zone not in cost_so_far or new_cost < cost_so_far[next_zone]:
                    cost_so_far[next_zone] = new_cost
                    priority = new_cost
                    frontier.put(next_zone, priority)
                    came_from[next_zone] = current

        return came_from, cost_so_far
