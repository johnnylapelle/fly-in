from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QMainWindow

from ..graph import Graph
from .graph_scene import GraphScene
from .graph_view import GraphView


class MainWindow(QMainWindow):
    def __init__(self, graph: Graph) -> None:
        super().__init__()

        # self.setSize(1280, 720)
        self.setMinimumSize(1280, 720)
        view = GraphView()

        scene = GraphScene(graph)

        view.setScene(scene)
        self.setCentralWidget(view)
