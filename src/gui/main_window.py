from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QMainWindow,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget)

from ..core.exception import ConfigFileError
from ..core.graph import Graph
from ..io.map_loader import MapLoader
from ..pathfinding.pathfinding import Pathfinding
from ..simulation.simulator import Simulator
from .graph_scene import GraphScene
from .graph_view import GraphView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self._setup_ui()
        self.map_loader = MapLoader()
        self.map_loader.parse("maps/easy/01_linear_path.txt")
        self._load_state()

    def _load_state(self):
        self._drones = self.map_loader.drones
        self._zones = self.map_loader.zones
        self._connections = self.map_loader.connections

        self._graph = Graph(
            self._zones, self._connections
        )

        self._scene = GraphScene(self._graph, self._drones)
        self._view.setScene(self._scene)
        self.drones_items = self._scene.drones_items

        self._pathfinder = Pathfinding(self._graph, self._drones)
        self._pathfinder.compute_path()

        self._simulator = Simulator(
            self._graph, self._drones, self.drones_items)

    def _setup_ui(self) -> None:
        # central widget that contain the layout
        central = QWidget()

        # layout that contain the view and the panel
        layout = QHBoxLayout()
        layout.addWidget(self._create_view(), stretch=4)
        layout.addWidget(self._create_panel(), stretch=1)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def _create_view(self) -> GraphView:
        self._view = GraphView()
        return self._view

    def _create_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout()

        self.btn_load_map = QPushButton("Load a map")
        self.btn_load_map.clicked.connect(self._load_map_button_clicked)
        layout.addWidget(self.btn_load_map)

        self.btn_show_hide_desc = QPushButton("Show/Hide description")
        self.btn_show_hide_desc.clicked.connect(
            lambda: self._scene.toggle_labels)
        layout.addWidget(self.btn_show_hide_desc)

        self.btn_simulate = QPushButton("Simulate")
        self.btn_simulate.clicked.connect(lambda: self._simulator.simulate())
        layout.addWidget(self.btn_simulate)

        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(lambda: self._simulator.increase_turn())
        layout.addWidget(self.btn_next)

        self.btn_prev = QPushButton("Prev")
        self.btn_prev.clicked.connect(lambda: self._simulator.decrease_turn())
        layout.addWidget(self.btn_prev)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(
            lambda: self._simulator.reset_simulation())
        layout.addWidget(self.btn_reset)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def _load_map_button_clicked(self):
        try:
            self._load_map()
        except ConfigFileError as e:
            print(e)
            QMessageBox.warning(self, "ConfigFileError", str(e))

    def _load_map(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load a map",
            directory="maps/easy",
            filter="Txt (*.txt)"
        )

        if path:
            self.map_loader.parse(path)
            self._load_state()
