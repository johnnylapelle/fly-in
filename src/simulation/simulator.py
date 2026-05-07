from ..core.drone import Drone
from ..core.graph import Graph


class Simulator():
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self._drones: list[Drone] = drones
        self._graph: Graph = graph
        self._logs: str = ""
        self._turn: int = 0

    def simulate(self) -> None:
        # loop until all drones's finished and simulate everything
        self.reset_simulation()
        while self._is_everyone_done() is False:
            # print(f"turn={self._turn}")
            self._turn += 1
            self._execute_turn()
            self._print_logs()

    def _execute_turn(self) -> None:
        for drone in self._drones:
            try:
                zone, turn = drone.path[self._turn]

                if drone.position != zone:
                    self._logs += f"D{drone.id}-{zone} "

                drone.position = zone
            except IndexError:
                continue

    def _is_everyone_done(self) -> bool:
        # check if every drone is on the end zone
        for drone in self._drones:
            if drone.position != self._graph.end:
                return False
        return True

    def _print_logs(self) -> None:
        # print and reset logs from self._logs
        print(self._logs)
        self._logs = ""

    def reset_simulation(self) -> None:
        for drone in self._drones:
            drone.position = self._graph.start
            self._turn = 0
