from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

from ..core.drone import Drone
from ..core.graph import Graph
from ..simulation.simulator import Simulator
from .drone_item import DroneItem
from .graph_scene import GraphScene
from .graph_view import GraphView


class MainWindow(QMainWindow):
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        super().__init__()
        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self._scene = GraphScene(graph, drones)
        self.drones_items: list[DroneItem] = self._scene.drones_items
        self._simulator = Simulator(graph, drones, self.drones_items)
        self._setup_ui()

    def _setup_ui(self) -> None:
        # central widget that contain the layout
        central = QWidget()

        # layout that contain the view and the panel
        layout = QHBoxLayout()
        layout.addWidget(self._create_view(), stretch=5)
        layout.addWidget(self._create_panel(), stretch=1)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def _create_view(self) -> GraphView:
        view = GraphView()
        view.setScene(self._scene)
        return view

    def _create_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout()

        button_show_hide_desc = QPushButton("Show/Hide description")
        button_show_hide_desc.clicked.connect(self._scene.toggle_labels)
        layout.addWidget(button_show_hide_desc)

        button_simulate = QPushButton("Simulate")
        button_simulate.clicked.connect(self._simulator.simulate)
        layout.addWidget(button_simulate)

        button_next = QPushButton("Next")
        button_next.clicked.connect(self._simulator.increase_turn)
        layout.addWidget(button_next)

        button_prev = QPushButton("Prev")
        button_prev.clicked.connect(self._simulator.decrease_turn)
        layout.addWidget(button_prev)

        button_reset = QPushButton("Reset")
        button_reset.clicked.connect(self._simulator.reset_simulation)
        layout.addWidget(button_reset)

        layout.addStretch()
        panel.setLayout(layout)
        return panel
