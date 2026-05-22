from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem

from ..core.connection import Connection
from .utils import SCALE


class ConnectionItem(QGraphicsLineItem):
    """
    Graphical representation of a connection between two zones.

    Renders as a dashed grey line between the two zone positions,
    with the connection's maximum capacity displayed at the midpoint.
    """

    def __init__(self, connection: Connection):
        """
        Args:
            connection: The connection to render.
        """

        super().__init__()

        pen = self.init_pen()
        self.co = connection
        self.setLine(
            self.co.zone_a.x * SCALE,
            self.co.zone_a.y * SCALE,
            self.co.zone_b.x * SCALE,
            self.co.zone_b.y * SCALE
        )

        self.setPen(pen)

        # display the max_capacity
        info_capacity = str(self.co.max_capacity)
        self.desc = QGraphicsTextItem(self)
        self.desc.setHtml(
            f"<center>{info_capacity}</center>")
        line = self.line()
        mid_x = (line.x1() + line.x2()) / 2
        mid_y = (line.y1() + line.y2()) / 2
        rect = self.desc.boundingRect()
        self.desc.setPos(
            mid_x - rect.width() / 2, mid_y - rect.height() / 2)
        self.desc.setDefaultTextColor(QColor("black"))

    def init_pen(self) -> QPen:
        """
        Creates and returns the pen used to draw the connection line.

        Returns:
            A grey dashed QPen with a width of 3.
        """

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("grey"))
        pen.setStyle(Qt.PenStyle.DashLine)

        return pen
