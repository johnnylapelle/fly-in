import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent, QKeySequence, QResizeEvent, QShortcut
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMainWindow,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget)

from ..core.exception import ConfigFileError
from ..core.graph import Graph
from ..io.map_loader import MapLoader
from ..pathfinding.pathfinding import Pathfinding
from ..simulation.simulator import Simulator
from .graph_scene import GraphScene
from .graph_view import GraphView
from .utils import MARGIN


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self._setup_ui()
        self.map_loader = MapLoader()
        self.map_loader.parse("maps/easy/01_linear_path.txt")
        # self.map_loader.parse("maps/challenger/01_the_impossible_dream.txt")
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
                self._graph, self._drones, self.drones_items, self._res_table)
            self._simulator.turn_changed.connect(self._update_turn_label)
        except Exception as e:
            print(e)
            QMessageBox.warning(
                self, "Error", f"{str(e)}\nThe program will exit.")
            sys.exit(1)

    def _setup_ui(self) -> None:
        # central widget that contain the layout
        central = QWidget()

        # layout that contain the view and the panel
        layout = QHBoxLayout()

        self._view = self._create_view()
        layout.addWidget(self._view)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self._setup_turn_label()
        self._create_overlay_panel()
        self._setup_sim_panel()

        self._setup_shortcut()

        QTimer.singleShot(0, self._update_sim_panel)

    def _create_view(self) -> GraphView:
        self._view = GraphView()
        return self._view

    def _setup_turn_label(self) -> None:
        self._turn_label = QLabel(self)

        self._turn_label.setText("Turn 0\nDrones 0")
        self._turn_label.setStyleSheet("""
                font-size: 25px;
                color: black;
                font-family: "Cantarell";""")
        self._turn_label.adjustSize()

    def _create_overlay_panel(self) -> None:
        panel = QWidget(self._view)
        panel.setGeometry(10, 10, 180, 300)

        layout = QVBoxLayout(panel)

        self.btn_load_map = QPushButton("Load a map (M)")
        self.btn_load_map.clicked.connect(self._load_map_button_clicked)
        layout.addWidget(self.btn_load_map)

        self.btn_desc = QPushButton("Hide description (H)")
        self.btn_desc.clicked.connect(self._toggle_labels)
        layout.addWidget(self.btn_desc)

        self.btn_reset = QPushButton("Reset (R)")
        self.btn_reset.clicked.connect(
            lambda: self._simulator.reset_simulation())
        layout.addWidget(self.btn_reset)

        layout.addStretch()

        panel.setLayout(layout)
        panel.raise_()

    def _setup_sim_panel(self) -> None:
        self._sim_panel = QWidget(self)
        layout = QHBoxLayout(self._sim_panel)

        self.btn_prev = QPushButton("Prev (Left Arrow)")
        self.btn_prev.clicked.connect(
            lambda: self._simulator.increase_decrease_turn(-1))
        layout.addWidget(self.btn_prev)

        self.btn_simulate = QPushButton("Simulate (Space)")
        self.btn_simulate.clicked.connect(lambda: self._simulator.toggle())
        layout.addWidget(self.btn_simulate)

        self.btn_next = QPushButton("Next (Right Arrow)")
        self.btn_next.clicked.connect(
            lambda: self._simulator.increase_decrease_turn(1))
        layout.addWidget(self.btn_next)

        self._sim_panel.setLayout(layout)
        self._sim_panel.raise_()

    def _setup_shortcut(self) -> None:
        try:
            shortcut_right = QShortcut(QKeySequence("Right"), self)
            shortcut_right.activated.connect(
                lambda: self._simulator.increase_decrease_turn(1))

            shortcut_left = QShortcut(QKeySequence("Left"), self)
            shortcut_left.activated.connect(
                lambda: self._simulator.increase_decrease_turn(-1))

            shortcut_space = QShortcut(QKeySequence("Space"), self)
            shortcut_space.activated.connect(
                lambda: self._simulator.toggle())

            shortcut_r = QShortcut(QKeySequence("R"), self)
            shortcut_r.activated.connect(
                lambda: self._simulator.reset_simulation())

            shortcut_escape = QShortcut(QKeySequence("Escape"), self)
            shortcut_escape.activated.connect(
                lambda: self.close())

            shortcut_m = QShortcut(QKeySequence("M"), self)
            shortcut_m.activated.connect(
                self._load_map_button_clicked)

            shortcut_h = QShortcut(QKeySequence("H"), self)
            shortcut_h.activated.connect(
                self._toggle_labels)

        except Exception:
            print("Error")

    def _load_map_button_clicked(self) -> None:
        try:
            self._load_map()
            self._update_turn_label(0)
        except ConfigFileError as e:
            print(e)
            QMessageBox.warning(self, "ConfigFileError", str(e))

    def _load_map(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load a map",
            directory="maps/easy",
            filter="Txt (*.txt)"
        )

        if path:
            self.map_loader.parse(path)
            self._load_state()

    def _toggle_labels(self) -> None:
        self._scene.toggle_labels()
        self._labels_visible = not self._labels_visible

        if self._labels_visible:
            self.btn_desc.setText("Hide description (H)")
        else:
            self.btn_desc.setText("Show description (H)")

    def _update_turn_label(self, turn: int) -> None:
        self._turn_label.setText(
            f"     Turn: {turn}\nDrones: {self.map_loader.nb_drones}")

        self._turn_label.adjustSize()

        self._turn_label.move(
            self.width() - self._turn_label.width() - MARGIN - 30,
            MARGIN)

    def _update_sim_panel(self) -> None:
        self._sim_panel.adjustSize()

        w = self._sim_panel.width()
        h = self._sim_panel.height()

        vw = self._view.width()
        vh = self._view.height()

        self._sim_panel.move(
            (vw - w) // 2, vh - h - MARGIN)

    def keyPressEvent(self, event: QKeyEvent | None):
        if event is None:
            return

        if event.key() == Qt.Key.Key_Left:
            self._simulator.increase_decrease_turn(-1)
        if event.key() == Qt.Key.Key_Right:
            self._simulator.increase_decrease_turn(1)

        super().keyPressEvent(event)

    def resizeEvent(self, a0: QResizeEvent | None):
        try:
            self._update_turn_label(self._simulator.turn)
        except AttributeError:
            self._update_turn_label(0)

        self._update_sim_panel()

        return super().resizeEvent(a0)
