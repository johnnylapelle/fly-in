from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

from ..core.graph import Graph
from .graph_scene import GraphScene
from .graph_view import GraphView


class MainWindow(QMainWindow):
    def __init__(self, graph: Graph) -> None:
        super().__init__()
        self.setWindowTitle("Fly-in")
        self.setMinimumSize(1280, 720)
        self._scene = GraphScene(graph)
        self._setup_ui()

    def _setup_ui(self) -> None:
        # central widget that contain the layout
        central = QWidget()

        # layout that contain the view and the panel
        layout = QHBoxLayout()
        layout.addWidget(self._create_view(), stretch=2)
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

        layout.addStretch()
        panel.setLayout(layout)
        return panel
