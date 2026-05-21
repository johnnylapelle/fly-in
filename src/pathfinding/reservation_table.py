from ..core.graph import Graph


class ReservationTable:
    """
    Tracks zone and connection occupancy across turns.

    Used by the pathfinding algorithm to enforce capacity constraints.
    Each entry records how many drones have reserved a given location
    at a given turn. A location is considered unavailable when its
    current reservation count reaches its maximum capacity.
    """

    def __init__(self, graph: Graph):
        """
        Args:
            graph: The graph, used to look up maximum capacities for
                zones and connections by name.
        """

        self._graph = graph
        self.reservations: dict[tuple[str, int], int] = {}

    def is_available(self, name: str, turn: int) -> bool:
        """
        Returns True if the location has remaining capacity at the given turn.

        Args:
            name: The name of the zone or connection key.
            turn: The turn to check availability for.

        Returns:
            True if current reservations are below maximum capacity,
            False otherwise.
        """

        max_capacity = self._graph.get_max_capacity(name)
        current = self.reservations.get((name, turn), 0)
        if current >= max_capacity:
            return False
        return True

    def reserve(self, name: str, turn: int) -> None:
        """
        Increments the reservation count for a location at a given turn.

        Args:
            name: The name of the zone or connection key to reserve.
            turn: The turn at which the location is reserved.
        """

        current = self.reservations.get((name, turn), 0)
        self.reservations[(name, turn)] = current + 1
