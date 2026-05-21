from typing import Any, Union

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.exception import PathfindingError
from ..core.graph import Graph
from ..core.zone import Zone
from .priority_queue import PriorityQueue
from .reservation_table import ReservationTable

Node = Union[Zone | Connection]


class Pathfinding:
    """
    Computes collision-free paths for all drones using Space-Time A*.

    First runs a reverse Dijkstra from the end zone to build an admissible
    heuristic for every zone. Then processes each drone sequentially,
    running Space-Time A* and reserving the resulting path in a shared
    reservation table so subsequent drones route around it.
    """

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """
        Initializes the pathfinder and computes the heuristic.

        Runs reverse Dijkstra immediately on construction. Raises
        PathfindingError if the end zone is unreachable from the start.

        Args:
            graph: The graph to pathfind through.
            drones: List of drones to compute paths for.
        """

        self._graph = graph
        self._drones = drones
        self._heuristic: dict[Zone, float] = {}
        self._reverse_dijkstra()
        self._res_table = ReservationTable(self._graph)

    @property
    def res_table(self) -> ReservationTable:
        """The shared reservation table built during path computation."""

        return self._res_table

    def compute_path(self) -> None:
        """
        Computes and assigns a path to each drone sequentially.

        Each drone starts at the graph's start zone. Paths are computed
        one by one — each drone is constrained by the reservations left
        by previously processed drones.

        Also builds drone.sim_path, a filtered version of the full path
        containing only zones and restricted connections, used by the
        simulator for animation.
        """

        start = self._graph.start

        for drone in self._drones:
            drone.position = start
            start.current_nb_drone += 1
            drone.path = self._space_time_a_star()
            drone._sim_path = [(node, t) for node, t in drone.path
                               if isinstance(node, Zone) or
                               (isinstance(node, Connection)
                                and node.is_restricted)]

    def _reverse_dijkstra(self) -> None:
        """
        Computes the heuristic for every zone via reverse Dijkstra.

        Runs Dijkstra from the end zone backwards through the graph,
        ignoring temporal constraints and blocked zones. The resulting
        cost for each zone represents the minimum distance to the
        destination and serves as an admissible heuristic for A*.
        """

        start = self._graph.end
        goal = self._graph.start
        frontier: PriorityQueue[Any] = PriorityQueue()
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

    def _space_time_a_star(self) -> list[tuple[Node, int]]:
        """
        Finds the optimal path for one drone using Space-Time A*.

        Operates on (zone, turn) states to account for temporal
        constraints. At each state, the drone can either move to a
        neighboring zone or wait in place. Movements are only considered
        if both the connection and the destination zone are available in
        the reservation table at the relevant turn.

        Connections are stored as intermediate states in the path to
        allow the reservation table to track their occupancy.

        Returns:
            A list of (node, turn) tuples representing the full path,
            including intermediate connection states.
        """

        path: dict[tuple[Node, int], tuple[Node, int] | None] = {}
        cost_so_far: dict[tuple[Node, int], int] = {}
        open_list: PriorityQueue[Any] = PriorityQueue()
        closed_set: set[tuple[Node, int]] = set()

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
                        transit_state = (connection, turn)
                        path[transit_state] = current_state
                        path[next_state] = transit_state

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
            path: dict[tuple[Node, int],
                       tuple[Node, int] | None],
            turn: int,
            goal: Zone) -> list[tuple[Node, int]]:
        """
        Reconstructs the full path by backtracking through parent states.

        Follows the chain of parent pointers from (goal, turn) back to
        the start state (None), then reverses the result.

        Args:
            path: Dictionary mapping each state to its parent state.
            turn: The turn at which the goal was reached.
            goal: The destination zone.

        Returns:
            The ordered list of (node, turn) states from start to goal.
        """

        correct_path: list[tuple[Node, int]] = []
        current: tuple[Node, int] | None = (goal, turn)

        if (goal, turn) not in path:
            raise PathfindingError("(space_time_a_star) No solution found.")

        while current is not None:
            correct_path.append(current)
            current = path[current]

        correct_path.reverse()
        return correct_path

    def _reserve_path(self, path: list[tuple[Node, int]]) -> None:
        """
        Reserves all zones and connections in the path.

        Each (node, turn) pair is registered in the reservation table.
        Zones are reserved by name, connections by key. This prevents
        subsequent drones from occupying the same location at the same
        turn.

        Args:
            path: The full path returned by _reconstruct_path.
        """

        for item, turn in path:
            if isinstance(item, Zone):
                self._res_table.reserve(item.name, turn)
            else:
                self._res_table.reserve(item.key, turn)
