from .connection import Connection
from .exception import GraphError
from .zone import Zone


class Graph():
    """
    Represents the airspace graph of zones and connections.

    Builds an adjacency list on construction for efficient neighbor
    lookups. Caches the start and end zones. Provides cost and capacity
    queries used by the pathfinding algorithm.
    """

    def __init__(self, zones: dict[str, Zone],
                 connections: dict[str, Connection]) -> None:
        """
        Args:
            zones: All zones in the graph, keyed by name.
            connections: All connections in the graph, keyed by key.
        """

        self._zones: dict[str, Zone] = zones
        self._connections: dict[str, Connection] = connections
        self._adjacency: dict[str, list[Connection]] = {}
        self._start = self._find_start()  # caching of start
        self._end = self._find_end()  # caching of end
        self._build_adjacency()

    @property
    def start(self) -> Zone:
        """The unique start zone of the graph."""

        return self._start

    @property
    def end(self) -> Zone:
        """The unique end zone of the graph."""

        return self._end

    @property
    def zones(self) -> dict[str, Zone]:
        """All zones in the graph, keyed by name."""

        return self._zones

    @property
    def connections(self) -> dict[str, Connection]:
        """All connections in the graph, keyed by key."""

        return self._connections

    @property
    def adjacency(self) -> dict[str, list[Connection]]:
        """Adjacency list mapping each zone name to its connections."""

        return self._adjacency

    def _build_adjacency(self) -> None:
        """Populates the adjacency list from all connections."""

        for connection in self._connections.values():
            self._adjacency.setdefault(
                connection.zone_a.name, []).append(connection)

            self._adjacency.setdefault(
                connection.zone_b.name, []).append(connection)

    def _find_start(self) -> Zone:
        """
        Returns the start zone.
        """

        for zone in self._zones.values():
            if zone.is_start is True:
                return zone
        raise GraphError("No start zone found.")

    def _find_end(self) -> Zone:
        """
        Returns the end zone.
        """

        for zone in self._zones.values():
            if zone.is_end is True:
                return zone
        raise GraphError("No end zone found.")

    def get_neighbours(self, zone: Zone) -> list[Connection]:
        """
        Returns all connections adjacent to the given zone.

        Args:
            zone: The zone to query.

        Returns:
            A list of connections, or an empty list if the zone
            has no neighbors.
        """

        return self._adjacency.get(zone.name, [])

    def cost(self, zone: Zone) -> float:
        """
        Returns the traversal cost for entering a zone.

        Costs by zone type: normal = 1, priority = 0.99,
        restricted = 2, blocked = very large number.

        Args:
            zone: The zone to query.

        Returns:
            The traversal cost as a float.
        """

        if zone.type == "restricted":
            return 2
        elif zone.type == "blocked":
            return 100000000000000000000000000000000
        elif zone.type == "normal":
            return 1
        elif zone.type == "priority":
            return 0.99
        else:
            raise GraphError("Unknown zone type")

    def get_max_capacity(self, name: str) -> int:
        """
        Returns the maximum drone capacity for a zone or connection.

        Args:
            name: A zone name or connection key.

        Returns:
            The maximum capacity as an integer.
        """

        if name in self._connections:
            return self._connections[name].max_capacity
        if name in self._zones:
            return self._zones[name].max_drones
        raise GraphError(f"'{name} not found in zones or connections.")
