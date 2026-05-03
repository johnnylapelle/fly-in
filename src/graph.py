from .connection import Connection
from .exception import GraphError
from .zone import Zone


class Graph():
    def __init__(self, zones: dict[str, Zone],
                 connections: dict[str, Connection]) -> None:
        self._zones: dict[str, Zone] = zones
        self._connections: dict[str, Connection] = connections
        self._adjacency: dict[str, list[Connection]] = {}
        self._start = self._find_start()  # caching of start
        self._end = self._find_end()  # caching of end
        self._build_adjacency()

    @property
    def start(self) -> Zone:
        return self._start

    @property
    def end(self) -> Zone:
        return self._end

    @property
    def zones(self) -> dict[str, Zone]:
        return self._zones

    @property
    def connections(self) -> dict[str, Connection]:
        return self._connections

    def _build_adjacency(self) -> None:
        # create the dict of adjacency
        for connection in self._connections.values():
            self._adjacency.setdefault(
                connection.zone_a.name, []).append(connection)

            self._adjacency.setdefault(
                connection.zone_b.name, []).append(connection)

    def get_neighbours(self, zone: Zone) -> list[Connection]:
        # return the neighbours of a zone
        return self._adjacency.get(zone.name, [])

    def _find_start(self) -> Zone:
        # find the start zone
        for zone in self._zones.values():
            if zone.is_start is True:
                return zone
        raise GraphError("No start zone found.")

    def _find_end(self) -> Zone:
        # find the end zone
        for zone in self._zones.values():
            if zone.is_end is True:
                return zone
        raise GraphError("No end zone found.")
