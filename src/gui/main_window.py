from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget, QFileDialog, QMessageBox)

from ..io.map_loader import MapLoader
# from ..core.drone import Drone
from ..core.graph import Graph
from ..simulation.simulator import Simulator
# from .drone_item import DroneItem
from .graph_scene import GraphScene
from .graph_view import GraphView
from ..core.exception import ConfigFileError


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self.map_loader = MapLoader()
        self._setup_ui()

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

        self._simulator = Simulator(
            self._graph, self._drones, self.drones_items)

        self.button_show_hide_desc.clicked.connect(self._scene.toggle_labels)
        self.button_simulate.clicked.connect(self._simulator.simulate)
        self.button_next.clicked.connect(self._simulator.increase_turn)
        self.button_prev.clicked.connect(self._simulator.decrease_turn)
        self.button_reset.clicked.connect(self._simulator.reset_simulation)

    def _setup_ui(self) -> None:
        # central widget that contain the layout
        central = QWidget()

        # layout that contain the view and the panel
        layout = QHBoxLayout()
        layout.addWidget(self._create_view(), stretch=3)
        layout.addWidget(self._create_panel(), stretch=1)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def _create_view(self) -> GraphView:
        self._view = GraphView()
        return self._view

    def _create_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout()

        self.button_load_map = QPushButton("Load a map")
        self.button_load_map.clicked.connect(self._load_map_button_clicked)
        layout.addWidget(self.button_load_map)

        self.button_show_hide_desc = QPushButton("Show/Hide description")
        layout.addWidget(self.button_show_hide_desc)

        self.button_simulate = QPushButton("Simulate")
        layout.addWidget(self.button_simulate)

        self.button_next = QPushButton("Next")
        layout.addWidget(self.button_next)

        self.button_prev = QPushButton("Prev")
        layout.addWidget(self.button_prev)

        self.button_reset = QPushButton("Reset")
        layout.addWidget(self.button_reset)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def _load_map_button_clicked(self):
        try:
            self.load_map()
        except ConfigFileError as e:
            print(e)
            QMessageBox.warning(self, "Error", str(e))

    def load_map(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load a map",
            directory="maps",
            filter="Txt (*.txt)"
        )

        if path:
            self.map_loader.parse(path)
            self._load_state()
