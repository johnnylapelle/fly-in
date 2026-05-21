from typing import Union

from PyQt6.QtCore import (QAbstractAnimation, QEasingCurve, QObject,
                          QPauseAnimation, QPointF, QPropertyAnimation,
                          pyqtSignal)

from ..core.connection import Connection
from ..core.drone import Drone
from ..core.graph import Graph
from ..core.zone import Zone
from ..gui.drone_item import DroneItem
from ..gui.utils import SCALE
from .simulation_state import SimulationState

Node = Union[Zone, Connection]


class Simulator(QObject):
    turn_changed = pyqtSignal(int)
    state_changed = pyqtSignal()

    def __init__(self, graph: Graph, drones: list[Drone],
                 drones_items: list[DroneItem],
                 debug: bool) -> None:

        super().__init__()

        self._drones: list[Drone] = drones
        self._graph: Graph = graph
        self._drones_items = drones_items

        self._debug = debug

        self.state = SimulationState.IDLE

        self.turn: int = 0
        self._max_turn: int = 0

        self.animations: list[QAbstractAnimation] = []

        self._pending_moves = 0
        self._current_logs: list[str] = []

        self._get_max_turn()

    def toggle(self) -> None:
        if self.state == SimulationState.IDLE:
            self._start()
        elif self.state == SimulationState.RUNNING:
            self._pause()
        elif self.state == SimulationState.PAUSED:
            self._resume()
        elif self.state == SimulationState.FINISHED:
            self.reset()

    def _start(self) -> None:
        self.state = SimulationState.RUNNING

        self._play_next_turn()

    def _pause(self) -> None:
        for anim in self.animations:
            if anim.state() == QAbstractAnimation.State.Running:
                anim.pause()

        self.state = SimulationState.PAUSED

    def _resume(self) -> None:
        for anim in self.animations:
            if anim.state() == QAbstractAnimation.State.Paused:
                anim.resume()

        self.state = SimulationState.RUNNING

    def _finish(self) -> None:
        self.state = SimulationState.FINISHED
        self.state_changed.emit()

    def increase_decrease_turn(self, n: int) -> None:

        if n == -1 and self.turn <= 0:
            return
        elif n == 1 and self.turn >= self._max_turn:
            return

        # change the state and icon to IDLE
        self.state = SimulationState.IDLE
        self.state_changed.emit()

        moves = self._get_moves(self.turn, self.turn + n)

        self.turn += n
        self.turn_changed.emit(self.turn)
        self._animate_step(moves)

    def _play_next_turn(self) -> None:
        if self.turn >= self._max_turn:
            self._finish()
            return

        moves = self._get_moves(self.turn, self.turn + 1)
        self.turn += 1
        self.turn_changed.emit(self.turn)
        self._animate_step(moves)

    def _get_moves(
            self,
            from_turn: int,
            to_turn: int) -> list[tuple[int, Node, Node]]:

        moves = []

        for i, drone in enumerate(self._drones):
            try:
                start_node = next(
                    node for node, t in drone.sim_path if t == from_turn and isinstance(node, Zone))
                end_node = next(
                    node for node, t in drone.sim_path if t == to_turn and isinstance(node, Zone))

                moves.append((i, start_node, end_node))
            except StopIteration:
                continue

        print(self.turn)
        return moves

    def _animate_step(
            self,
            moves: list[tuple[int, Node, Node]]) -> None:

        if not moves:
            return

        self._pending_moves = len(moves)
        self._current_logs.clear()

        for i, start_node, end_node in moves:
            drone_item = self._drones_items[i]

            anim = QPropertyAnimation(drone_item, b"pos")
            anim.setDuration(300)

            anim.setStartValue(self._get_pose(start_node))
            anim.setEndValue(self._get_pose(end_node))

            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.finished.connect(
                lambda i=i, node=end_node: self._on_move_finished(i, node)
            )

            anim.start()
            self.animations.append(anim)

    def _get_max_turn(self) -> None:
        for drone in self._drones:
            for item, turn in drone.sim_path:
                if turn > self._max_turn:
                    self._max_turn = turn

    def _get_pose(self, node: Zone | Connection) -> QPointF:
        if isinstance(node, Zone):
            return QPointF(node.x * SCALE, node.y * SCALE)

        elif isinstance(node, Connection):
            x = (node.zone_a.x + node.zone_b.x) / 2
            y = (node.zone_a.y + node.zone_b.y) / 2
            return QPointF(x * SCALE, y * SCALE)

    def _on_move_finished(self, idx: int, node: Node) -> None:
        drone = self._drones[idx]

        prev_position = drone.position
        drone.position = node

        if self._debug:
            self._track_node_stats(prev_position, node)

        if prev_position != node:
            self._current_logs.append(f"D{drone.id}-{node}")

        self._pending_moves -= 1

        if self._pending_moves == 0:
            print(f"Turn {self.turn}")
            print(" ".join(self._current_logs))

            if self._debug:
                self._print_node_stats()

            if self.state == SimulationState.RUNNING:
                pause = QPauseAnimation(200)
                pause.finished.connect(self._play_next_turn)
                pause.start()
                self.animations.append(pause)

    def reset(self) -> None:
        print()
        self.state = SimulationState.IDLE
        for anim in self.animations:
            anim.stop()

        self.animations.clear()

        self.turn = 0
        self._pending_moves = 0
        self._current_logs.clear()

        for drone in self._drones:
            drone.position = self._graph.start

        for drone_item in self._drones_items:
            drone_item.move()

        for zone in self._graph.zones.values():
            if zone.is_start:
                zone.current_nb_drone = len(self._drones)
            else:
                zone.current_nb_drone = 0

        for co in self._graph.connections.values():
            co.current_nb_drone = 0

    def _track_node_stats(self, leave: Node | None,
                          enter: Node | None) -> None:
        if leave is not None:
            leave.current_nb_drone -= 1
        if enter is not None:
            enter.current_nb_drone += 1

    def _print_node_stats(self) -> None:
        for zone in self._graph.zones.values():
            print(f"{zone.name} "
                  f"{zone.current_nb_drone}/{zone.max_drones}")
        print()
