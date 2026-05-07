from PyQt6.QtCore import (QEasingCurve, QPointF, QPropertyAnimation,
                          QSequentialAnimationGroup, QPauseAnimation)

from ..core.drone import Drone
from ..core.connection import Connection
from ..core.zone import Zone
from ..core.graph import Graph
from ..gui.drone_item import DroneItem
from ..gui.utils import SCALE


class Simulator():
    def __init__(self, graph: Graph, drones: list[Drone],
                 drones_items: list[DroneItem]) -> None:
        self._drones: list[Drone] = drones
        self._graph: Graph = graph
        self._drones_items = drones_items
        self._logs: str = ""
        self._turn: int = 0
        self._max_turn: int = 0
        self.get_max_turn()
        self.animations: list[QSequentialAnimationGroup] = []

    def simulate(self) -> None:
        # loop until all drones's finished and simulate everything
        self.reset_simulation()

        for anim in self.animations:
            anim.stop()
        self.animations.clear()

        for drone_item, drone, in zip(self._drones_items, self._drones):
            self.animate(drone_item, drone.path)

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
        self._logs = "\n"

        for anim in self.animations:
            anim.stop()
        self.animations.clear()

        for drone in self._drones:
            drone.position = self._graph.start

        self._turn = 0
        self._move_all_drone()

    def increase_turn(self) -> None:
        if self._turn < self._max_turn:
            self._turn += 1
        self._execute_turn_and_move()

    def decrease_turn(self) -> None:
        if self._turn > 0:
            self._turn -= 1
        self._execute_turn_and_move()

    def _execute_turn_and_move(self):
        self._execute_turn()
        self._move_all_drone()

    def _move_all_drone(self) -> None:
        for drone in self._drones_items:
            drone.move()

    def get_max_turn(self) -> None:
        for drone in self._drones:
            for item, turn in drone.path:
                if turn > self._max_turn:
                    self._max_turn = turn

    def animate(self, drone_item, path) -> None:
        if len(path) < 2:
            return

        group = QSequentialAnimationGroup()

        for i in range(len(path) - 1):
            (start_node, _), (end_node, _) = path[i], path[i + 1]

            anim = QPropertyAnimation(drone_item, b"pos")
            anim.setDuration(300)

            anim.setStartValue(self.get_pose(start_node))

            anim.setEndValue(self.get_pose(end_node))

            anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

            group.addAnimation(anim)

            pause = QPauseAnimation()
            pause.setDuration(200)
            group.addAnimation(pause)

        self.animations.append(group)
        group.start()

    def get_pose(self, node: Zone | Connection) -> QPointF:
        if isinstance(node, Zone):
            return QPointF(node.x * SCALE, node.y * SCALE)

        elif isinstance(node, Connection):
            x = (node.zone_a.x + node.zone_b.x / 2)
            y = (node.zone_a.y + node.zone_b.y / 2)
            return QPointF(x * SCALE, y * SCALE)
