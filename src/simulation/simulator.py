from ..core.drone import Drone
from ..core.graph import Graph


class Simulator():
    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self._drones: list[Drone] = drones
        self._graph: Graph = graph
        self._logs: str = ""
        self._turn: int = 0

    def simulate(self) -> None:
        # loop until all drones's finished and simulate everything
        while self._is_everyone_done() is False:
            self._execute_turn()
            break

    def _execute_turn(self) -> None:
        # execute a single turn
        pass

    def _is_everyone_done(self) -> bool:
        # check if every drone is on the end zone
        for drone in self._drones:
            if not drone._is_arrived:
                return False
        return True

    def _print_logs(self) -> None:
        # print and reset logs from self._logs
        print(self._logs)
        self._logs = ""
