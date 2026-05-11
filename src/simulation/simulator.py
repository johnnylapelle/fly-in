from typing import Union

from PyQt6.QtCore import (QAbstractAnimation, QEasingCurve, QPauseAnimation,
                          QPointF, QPropertyAnimation,
                          QSequentialAnimationGroup)

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.graph import Graph
from ..core.zone import Zone
from ..gui.drone_item import DroneItem
from ..gui.utils import SCALE

StateKey = Union[Zone, Connection]


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
        self.animations: list[QAbstractAnimation] = []

    def simulate(self) -> None:
        # loop until all drones's finished and simulate everything
        self.reset_simulation()

        for anim in self.animations:
            anim.stop()
        self.animations.clear()

        for i, (drone_item, drone) in enumerate(
         zip(self._drones_items, self._drones)):
            print("test")
            self.animate(i, drone_item, drone.path)

        print(self._turn)

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

        for drone_item in self._drones_items:
            drone_item.move()

    def increase_turn(self) -> None:
        if self._turn >= self._max_turn:
            return

        moves = []
        for i, drone in enumerate(self._drones):
            try:
                start_node, _ = drone.path[self._turn]
                end_node, _ = drone.path[self._turn + 1]
                moves.append((i, start_node, end_node))
            except IndexError:
                continue

        self._turn += 1
        self._execute_turn()
        self._animate_step(moves)

    def decrease_turn(self) -> None:
        if self._turn <= 0:
            return

        moves = []
        for i, drone in enumerate(self._drones):
            try:
                start_node, _ = drone.path[self._turn]
                end_node, _ = drone.path[self._turn - 1]
                moves.append((i, start_node, end_node))
            except IndexError:
                continue

        self._turn -= 1
        self._execute_turn()
        self._animate_step(moves)

    def _animate_step(
            self,
            moves: list[tuple[int, StateKey, StateKey]]) -> None:

        for i, start_node, end_node in moves:
            drone_item = self._drones_items[i]
            anim = QPropertyAnimation(drone_item, b"pos")
            anim.setDuration(300)
            anim.setStartValue(self.get_pose(start_node))
            anim.setEndValue(self.get_pose(end_node))
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.start()
            self.animations.append(anim)

    def get_max_turn(self) -> None:
        for drone in self._drones:
            for item, turn in drone.path:
                if turn > self._max_turn:
                    self._max_turn = turn

    def animate(
            self,
            idx: int,
            drone_item: DroneItem,
            path: list[tuple[StateKey, int]]) -> None:

        if len(path) < 2:
            return

        group = QSequentialAnimationGroup()

        for i in range(len(path) - 1):
            (start_node, _), (end_node, _) = path[i], path[i + 1]

            anim = QPropertyAnimation(drone_item, b"pos")
            anim.setDuration(300)

            anim.setStartValue(self.get_pose(start_node))

            anim.setEndValue(self.get_pose(end_node))

            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

            group.addAnimation(anim)

            pause = QPauseAnimation()
            pause.setDuration(200)
            group.addAnimation(pause)

        group.currentAnimationChanged.connect(
            lambda _, idx=idx: self._sync_drone_pose(idx))

        self.animations.append(group)
        group.start()

    def get_pose(self, node: Zone | Connection) -> QPointF:
        if isinstance(node, Zone):
            return QPointF(node.x * SCALE, node.y * SCALE)

        elif isinstance(node, Connection):
            x = (node.zone_a.x + node.zone_b.x) / 2
            y = (node.zone_a.y + node.zone_b.y) / 2
            return QPointF(x * SCALE, y * SCALE)

    def _sync_drone_pose(self, idx: int) -> None:
        drone = self._drones[idx]

        if self._turn < self._max_turn:
            self._turn += 1

        if self._turn < len(drone.path):
            node, _ = drone.path[idx]
            drone.position = node
        print(self._turn)
