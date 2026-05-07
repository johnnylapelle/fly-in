from typing import Union

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.exception import PathfindingError
from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue
from .reservation_table import ReservationTable


StateKey = Union[Zone | Connection]


class Pathfinding:

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self._graph = graph
        self._drones = drones
        self._heuristic: dict[Zone, float] = {}
        self._reverse_dijkstra()
        self._res_table = ReservationTable(self._graph)

    def compute_path(self):
        start = self._graph.start

        for drone in self._drones:
            drone.position = start
            drone.path = self._space_time_a_star()
            print(drone.path)

    def _reverse_dijkstra(self) -> None:
        start = self._graph.end
        goal = self._graph.start
        frontier: PriorityQueue = PriorityQueue()
        frontier.put(start, 0)
        self._heuristic[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for connection in self._graph.get_neighbours(current):
                next_zone = connection.get_other(current)
                new_cost = (self._heuristic[current]
                            + self._graph.cost(next_zone))

                if next_zone.type == "blocked":
                    continue

                if (next_zone not in self._heuristic
                   or new_cost < self._heuristic[next_zone]):
                    self._heuristic[next_zone] = new_cost
                    priority = new_cost
                    frontier.put(next_zone, priority)

        if goal not in self._heuristic:
            raise PathfindingError(
                "(reverse_dijkstra) No solution found.")

    def _space_time_a_star(self) -> list[tuple[StateKey, int]]:

        path: dict[tuple[StateKey, int], tuple[StateKey, int] | None] = {}
        cost_so_far: dict[tuple[StateKey, int], int] = {}
        open_list: PriorityQueue = PriorityQueue()
        closed_set: set[tuple[StateKey, int]] = set()

        start = self._graph.start
        goal = self._graph.end
        start_state = (start, 0)

        cost_so_far[start_state] = 0
        path[start_state] = None
        open_list.put((start, 0, 0), priority=self._heuristic[start])

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

                if next_zone.type == "blocked":
                    continue

                move_cost = self._graph.cost(next_zone)
                arrival_turn = turn + round(move_cost)
                new_cost = g + round(move_cost)

                next_state = (next_zone, arrival_turn)

                if not self._res_table.is_available(connection.key, turn):
                    continue
                if not self._res_table.is_available(
                 next_zone.name, arrival_turn):
                    continue

                if (next_state not in cost_so_far
                   or new_cost < cost_so_far[next_state]):

                    f = new_cost + self._heuristic[next_zone]

                    cost_so_far[next_state] = new_cost
                    open_list.put(
                        (next_zone, arrival_turn, new_cost), priority=f)

                    if next_zone.type == "restricted":
                        transit_state = (connection, turn + 1)
                        path[transit_state] = (current_state)
                        path[next_state] = transit_state
                    else:
                        path[next_state] = current_state

            # wait action
            wait_state = (current, turn + 1)

            if (current.is_start
               or self._res_table.is_available(current.name, turn + 1)):

                wait_cost = g + 1

                if (wait_state not in cost_so_far
                   or wait_cost < cost_so_far[wait_state]):

                    cost_so_far[wait_state] = wait_cost
                    f = wait_cost + self._heuristic[current]
                    open_list.put((current, turn + 1, wait_cost), priority=f)
                    path[wait_state] = (current, turn)

        correct_path = self._reconstruct_path(path, turn, goal)
        self._reserve_path(correct_path)
        return correct_path

    def _reconstruct_path(
            self,
            path: dict[tuple[StateKey, int],
                       tuple[StateKey, int] | None],
            turn: int,
            goal: Zone) -> list[tuple[StateKey, int]]:

        correct_path: list[tuple[StateKey, int]] = []
        current: tuple[StateKey, int] | None = (goal, turn)

        if (goal, turn) not in path:
            raise PathfindingError("(space_time_a_star) No solution found.")

        while current is not None:
            correct_path.append(current)
            current = path[current]

        correct_path.reverse()
        return correct_path

    def _reserve_path(self, path: list[tuple[StateKey, int]]) -> None:
        for item, turn in path:
            if isinstance(item, Zone):
                self._res_table.reserve(item.name, turn)
            else:
                print(f"Connection={item.key}, turn={turn}")
                self._res_table.reserve(item.key, turn)
