from ..core.graph import Graph


class ReservationTable:
    def __init__(self, graph: Graph):
        self._graph = graph
        self.reservations: dict[tuple[str, int], int] = {}

    def is_available(self, name: str, turn: int) -> bool:
        max_capacity = self._graph.get_max_capacity(name)
        current = self.reservations.get((name, turn), 0)
        if current >= max_capacity:
            return False
        return True

    def reserve(self, name: str, turn: int) -> None:
        current = self.reservations.get((name, turn), 0)
        current += 1
