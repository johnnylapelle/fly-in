import sys
import typing

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QKeySequence, QResizeEvent, QShortcut
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QMessageBox, QPushButton, QStyle,
                             QVBoxLayout, QWidget)

from ..core.exception import ConfigFileError
from .turn_label import TurnLabel
from .simulation_controls import SimControls
from .overlay_panel import OverlayPanel
from ..core.graph import Graph
from ..io.map_loader import MapLoader
from ..pathfinding.pathfinding import Pathfinding
from ..simulation.simulation_state import SimulationState
from ..simulation.simulator import Simulator
from .graph_scene import GraphScene
from .graph_view import GraphView
from .utils import MARGIN


class MainWindow(QMainWindow):
    def __init__(self, map_path: str | None, debug: bool) -> None:
        super().__init__()

        self._map_path = map_path
        self._debug = debug

        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self._setup_ui()
        self.map_loader = MapLoader()

        if self._map_path is not None:
            self.map_loader.parse(self._map_path)
            self._load_state()
        else:
            self.map_loader.parse("maps/easy/01_linear_path.txt")
            self._load_state()

        self._labels_visible = True

    def _load_state(self) -> None:
        try:
            self._drones = self.map_loader.drones
            self._zones = self.map_loader.zones
            self._connections = self.map_loader.connections

            self._graph = Graph(
                self._zones, self._connections)

            self._scene = GraphScene(self._graph, self._drones)
            self._view.setScene(self._scene)
            self.drones_items = self._scene.drones_items

            self._pathfinder = Pathfinding(self._graph, self._drones)
            self._pathfinder.compute_path()
            self._res_table = self._pathfinder.res_table

            self._simulator = Simulator(
                self._graph, self._drones,
                self.drones_items, self._debug)
            self._simulator.turn_changed.connect(self._update_turn_label)
            self._simulator.state_changed.connect(self._update_sim_controls)

        except Exception as e:
            print(e)
            QMessageBox.warning(
                self, "Error", f"{str(e)}\nThe program will exit.")
            sys.exit(1)

    def _setup_ui(self) -> None:
        central = QWidget()
        self._view = GraphView()
        QHBoxLayout(central).addWidget(self._view)
        self.setCentralWidget(central)

        self._turn_label = TurnLabel(self)
        self._overlay = OverlayPanel(self)
        self._sim_controls = SimControls(self)

        self._overlay.toggle_desc_requested.connect(
            self._toggle_labels)
        self._overlay.load_map_requested.connect(
            self._load_map_button_clicked)
        self._overlay.reset_requested.connect(
            lambda: self._simulator.reset())

        self._sim_controls.prev_requested.connect(
            lambda: self._simulator.increase_decrease_turn(-1))
        self._sim_controls.next_requested.connect(
            lambda: self._simulator.increase_decrease_turn(1))
        self._sim_controls.play_requested.connect(self._toggle_play)

        self._setup_shortcut()
        QTimer.singleShot(0, self._update_sim_controls)
        QTimer.singleShot(0, self._update_overlay)

    def _setup_shortcut(self) -> None:
        try:
            shortcut_right = QShortcut(QKeySequence("Right"), self)
            shortcut_right.activated.connect(
                lambda: self._simulator.increase_decrease_turn(1)
                if hasattr(self, '_simulator') else None)

            shortcut_left = QShortcut(QKeySequence("Left"), self)
            shortcut_left.activated.connect(
                lambda: self._simulator.increase_decrease_turn(-1)
                if hasattr(self, '_simulator') else None)

            shortcut_space = QShortcut(QKeySequence("Space"), self)
            shortcut_space.activated.connect(
                lambda: self._toggle_play()
                if hasattr(self, '_simulator') else None)

            shortcut_r = QShortcut(QKeySequence("R"), self)
            shortcut_r.activated.connect(
                lambda: self._simulator.reset()
                if hasattr(self, '_simulator') else None)

            shortcut_escape = QShortcut(QKeySequence("Escape"), self)
            shortcut_escape.activated.connect(
                lambda: self.close())

            shortcut_m = QShortcut(QKeySequence("M"), self)
            shortcut_m.activated.connect(
                self._load_map_button_clicked)

            shortcut_h = QShortcut(QKeySequence("H"), self)
            shortcut_h.activated.connect(
                self._toggle_labels)

        except AttributeError:
            print("Error")
            pass

    def _load_map_button_clicked(self) -> None:
        try:
            path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="Load a map",
                directory="maps/easy",
                filter="Txt (*.txt)"
            )

            if path:
                self.map_loader.parse(path)
                self._load_state()
                self._update_turn_label(0)
        except ConfigFileError as e:
            print(e)
            QMessageBox.warning(self, "ConfigFileError", str(e))

    def _toggle_labels(self) -> None:
        try:
            self._scene.toggle_labels()
            self._labels_visible = not self._labels_visible
            self._overlay.set_labels_visible(self._labels_visible)
        except AttributeError:
            pass

    def _toggle_play(self) -> None:
        self._simulator.toggle()

        self._sim_controls.set_playing(
            self._simulator.state)

    def _update_turn_label(self, turn: int) -> None:
        self._turn_label.setText(
            f"     Turn: {turn}     Drones: {self.map_loader.nb_drones}")

        self._turn_label.adjustSize()

        self._turn_label.move(
            self.width() - self._turn_label.width() - MARGIN - 30,
            MARGIN)

        self._turn_label.raise_()

    def _update_overlay(self) -> None:
        self._overlay.adjustSize()

        self._overlay.move(MARGIN, MARGIN)

        self._overlay.raise_()

    def _update_sim_controls(self) -> None:
        self._sim_controls.adjustSize()

        w = self._sim_controls.width()
        h = self._sim_controls.height()
        vw = self._view.width()
        vh = self._view.height()

        self._sim_controls.move(
            (vw - w) // 2, vh - h - MARGIN)

        self._sim_controls.set_playing(
            self._simulator.state)

        self._sim_controls.raise_()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        try:
            self._update_turn_label(self._simulator.turn)
        except AttributeError:
            self._update_turn_label(0)

        self._update_overlay()
        self._update_sim_controls()

        return super().resizeEvent(a0)
