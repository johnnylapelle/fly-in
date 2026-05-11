from ..core.graph import Graph


class ReservationTable:
    def __init__(self, graph: Graph):
        self._graph = graph
        self.reservations: dict[tuple[str, int], int] = {}

    def is_available(self, name: str, turn: int) -> bool:
        max_capacity = self._graph.get_max_capacity(name)
        current = self.reservations.get((name, turn), 0)
        if current >= max_capacity:
            # print(f"name={name}, turn={turn} FALSE")
            return False
        # print(f"name={name}, turn={turn} TRUE")
        return True

    def reserve(self, name: str, turn: int) -> None:
        current = self.reservations.get((name, turn), 0)
        self.reservations[(name, turn)] = current + 1

    def get_node_occupency(self, current_turn: int) -> list[str]:
        logs = []

        for key, occupency in self.reservations.items():
            name, turn = key

            max_cap = self._graph.get_max_capacity(name)

            if current_turn != turn:
                continue

            logs.append(f"{name} - {occupency}/{max_cap}")

        return logs
