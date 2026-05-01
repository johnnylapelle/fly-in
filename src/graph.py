from .zone import Zone
from .connection import Connection

class Graph():
    def __init__(self, zones: dict[str, Zone],
                 connections: dict[str, Connection]) -> None:
        self.zones = zones
        self.connections = connections
        self._adjacency: dict[str, list[Connection]] = {}
        self._build_adjacency()
        print(self._adjacency)

    def _build_adjacency(self) -> None:
        for connection in self.connections.values():
            self._adjacency.setdefault(
                connection.zone_a.name, []).append(connection)

            self._adjacency.setdefault(
                connection.zone_b.name, []).append(connection)

    def get_neighbours(self) -> list[Connection]:
        pass

    def get_start(self) -> Zone:
        pass

    def get_end(self) -> Zone:
        pass
