from ..core.drone import Drone
from ..core.graph import Graph


class Simulator():
    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self._drones: list[Drone] = drones
        self._graph: Graph = graph
        self._logs: str = ""
        self._turn: int = 1

    def simulate(self) -> None:
        # loop until all drones's finished and simulate everything
        while self._is_everyone_done() is False:
            # print(f"turn={self._turn}")
            self._execute_turn()
            self._print_logs()
            self._turn += 1
        # for drone in self._drones:
            # print(f"Drone: {drone.id}-{drone.position} is_arrived={drone.is_arrived}")

    def _execute_turn(self) -> None:
        for drone in self._drones:
            if drone.is_arrived:
                continue

            for zone, turn in drone.path:
                if turn == self._turn:
                    if drone.position != zone:
                        self._logs += f"D{drone.id}-{zone} "
                    drone.position = zone
                    break

            if drone.position == self._graph.end:
                drone.is_arrived = True

    def _is_everyone_done(self) -> bool:
        # check if every drone is on the end zone
        for drone in self._drones:
            if drone._is_arrived is False:
                return False
        return True

    def _print_logs(self) -> None:
        # print and reset logs from self._logs
        print(self._logs)
        self._logs = ""
