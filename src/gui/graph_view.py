from PyQt6.QtGui import QPainter, QWheelEvent
from PyQt6.QtWidgets import QGraphicsView


class GraphView(QGraphicsView):
    """
    Zoomable and pannable view for the graph scene.

    Supports scroll-to-zoom via the mouse wheel and click-to-pan via
    the scroll hand drag mode.
    """

    def __init__(self) -> None:
        """
        Zoomable and pannable view for the graph scene.

        Supports scroll-to-zoom via the mouse wheel and click-to-pan via
        the scroll hand drag mode.
        """

        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        """
        Zooms in or out by a factor of 1.15 on each wheel step.

        Args:
            event: The wheel event. Ignored if None.
        """
        factor = 1.15
        if isinstance(event, QWheelEvent):
            if event.angleDelta().y() > 0:
                self.scale(factor, factor)
            else:
                self.scale(1 / factor, 1 / factor)
