from .zone import Zone
from .connection import Connection

class Graph():
    def __init__(self, zones: dict[str, Zone],
                 connections: dict[str, Connection]) -> None:
        self.zones = zones
        self.connections = connections
        self.adjacency: dict[Zone, list[Connection]] = {}

    def _build_adjacency(self) -> dict[Zone, list[Connection]]:
        for connection in self.connections.values():
            self.adjacency.setdefault(
                connection.zone_a, []).append(connection)

            self.adjacency.setdefault(
                connection.zone_b, []).append(connection)

        return self.adjacency

    def get_neighbours(self) -> list[Connection]:
        pass

    def get_start(self) -> Zone:
        pass

    def get_end(self) -> Zone:
        pass
