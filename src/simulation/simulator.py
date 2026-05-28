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
    """
    Drives the step-by-step animation of drones moving through the graph.

    Reads pre-computed paths from each drone and animates their movement
    turn by turn using Qt property animations. Exposes playback controls
    (play, pause, resume, reset) and emits signals when the turn or state
    changes.

    Signals:
        turn_changed (int): Emitted whenever the current turn advances or
            moves backwards, carrying the new turn number.
        state_changed: Emitted when the simulation state changes
            (e.g. from RUNNING to FINISHED).
    """

    turn_changed = pyqtSignal(int)
    state_changed = pyqtSignal()

    def __init__(self, graph: Graph, drones: list[Drone],
                 drones_items: list[DroneItem],
                 debug: bool) -> None:
        """
        Args:
            graph: The graph the drones navigate through.
            drones: List of drones with pre-computed paths.
            drones_items: Corresponding Qt graphical items for each drone.
            debug: If True, prints zone occupancy stats after each turn.
        """

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
        """
        Toggles the simulation state machine.

        IDLE → RUNNING → PAUSED → RUNNING → FINISHED → IDLE.
        """

        if self.state == SimulationState.IDLE:
            self._start()
        elif self.state == SimulationState.RUNNING:
            self._pause()
        elif self.state == SimulationState.PAUSED:
            self._resume()
        elif self.state == SimulationState.FINISHED:
            self.reset()

    def _start(self) -> None:
        """Sets state to RUNNING and plays the first turn."""

        self.state = SimulationState.RUNNING

        self._play_next_turn()

    def _pause(self) -> None:
        """Pauses all running animations and sets state to PAUSED."""

        for anim in self.animations:
            if anim.state() == QAbstractAnimation.State.Running:
                anim.pause()

        self.state = SimulationState.PAUSED

    def _resume(self) -> None:
        """Resumes all paused animations and sets state to RUNNING."""

        for anim in self.animations:
            if anim.state() == QAbstractAnimation.State.Paused:
                anim.resume()

        self.state = SimulationState.RUNNING

    def _finish(self) -> None:
        """Sets state to FINISHED and emits state_changed."""

        self.state = SimulationState.FINISHED
        self.state_changed.emit()

    def increase_decrease_turn(self, n: int) -> None:
        """
        Moves the simulation forward or backward by n turns.

        Resets state to IDLE before animating. Does nothing if the
        resulting turn would be out of bounds.

        Args:
            n: Number of turns to advance (positive) or rewind (negative).
        """

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
        """
        Advances the simulation by one turn and triggers animation.
        Calls _finish if the last turn has been reached.
        """

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
        """
        Computes the list of drone movements between two turns.

        Looks up each drone's position at from_turn and to_turn in its
        sim_path, matching by turn value rather than list index.

        Args:
            from_turn: The turn to move from.
            to_turn: The turn to move to.

        Returns:
            A list of (drone_index, start_node, end_node) tuples.
        """

        moves = []

        for i, drone in enumerate(self._drones):
            try:
                start_node = next(
                    node for node, t in drone.sim_path if t == from_turn)
                end_node = next(
                    node for node, t in drone.sim_path if t == to_turn)

                moves.append((i, start_node, end_node))
            except StopIteration:
                continue

        return moves

    def _animate_step(
            self,
            moves: list[tuple[int, Node, Node]]) -> None:
        """
        Starts a QPropertyAnimation for each drone move.

        Each animation interpolates the drone's graphical item from its
        start position to its end position over 300ms. Calls
        _on_move_finished when each animation completes.

        Args:
            moves: List of (drone_index, start_node, end_node) tuples.
        """

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
        """
        Computes and stores the highest turn number across all drone paths.
        Used to determine when the simulation is finished.
        """

        for drone in self._drones:
            for item, turn in drone.sim_path:
                if turn > self._max_turn:
                    self._max_turn = turn

    def _get_pose(self, node: Zone | Connection) -> QPointF:
        """
        Returns the scene position of a node.

        For zones, returns the zone's coordinates scaled by SCALE.
        For connections, returns the midpoint between the two connected
        zones, scaled by SCALE.

        Args:
            node: A Zone or Connection instance.

        Returns:
            The corresponding QPointF position in the scene.
        """

        if isinstance(node, Zone):
            return QPointF(node.x * SCALE, node.y * SCALE)

        elif isinstance(node, Connection):
            x = (node.zone_a.x + node.zone_b.x) / 2
            y = (node.zone_a.y + node.zone_b.y) / 2
            return QPointF(x * SCALE, y * SCALE)

    def _on_move_finished(self, idx: int, node: Node) -> None:
        """
        Callback triggered when a drone animation completes.

        Updates the drone's position, logs the move if it changed, and
        decrements the pending move counter. When all moves for a turn
        are done, triggers the next turn if RUNNING, or prints debug
        stats if enabled.

        Args:
            idx: Index of the drone that finished moving.
            node: The node the drone has arrived at.
        """

        drone = self._drones[idx]

        prev_position = drone.position
        drone.position = node

        if self._debug:
            self._track_node_stats(prev_position, node)

        if prev_position != node:
            self._current_logs.append(f"D{drone.id}-{node}")

        self._pending_moves -= 1

        if self._pending_moves == 0:
            print(" ".join(self._current_logs))

            if self._debug:
                self._print_node_stats()

            if self.state == SimulationState.RUNNING:
                pause = QPauseAnimation(200)
                pause.finished.connect(self._play_next_turn)
                pause.start()
                self.animations.append(pause)

    def reset(self) -> None:
        """
        Resets the simulation to its initial state.

        Stops all animations, resets turn counter and drone positions,
        and restores zone and connection occupancy counts.
        """

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
        """
        Updates the current_nb_drone counter on nodes.

        Args:
            leave: The node the drone is leaving (decremented).
            enter: The node the drone is entering (incremented).
        """

        if leave is not None:
            leave.current_nb_drone -= 1
        if enter is not None:
            enter.current_nb_drone += 1

    def _print_node_stats(self) -> None:
        """Prints current drone occupancy for every zone in the graph."""

        for zone in self._graph.zones.values():
            print(f"{zone.name} "
                  f"{zone.current_nb_drone}/{zone.max_drones}")
        for co in self._graph.connections.values():
            print(f"{co.key} "
                  f"{co.current_nb_drone}/{co.max_capacity}")
        print()
