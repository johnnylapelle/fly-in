from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QWheelEvent
from .graph_scene import GraphScene

class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        factor = 1.15
        if isinstance(event, QWheelEvent):
            if event.angleDelta().y() > 0:
                self.scale(factor, factor)
            else:
                self.scale(1 / factor, 1 / factor)
