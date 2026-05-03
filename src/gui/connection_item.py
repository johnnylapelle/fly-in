from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem

from ..core.connection import Connection
from .utils import SCALE


class ConnectionItem(QGraphicsLineItem):
    def __init__(self, connection: Connection):
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
        self.label = QGraphicsTextItem(self)
        self.label.setHtml(
            f"<center>{info_capacity}</center>")
        line = self.line()
        mid_x = (line.x1() + line.x2()) / 2
        mid_y = (line.y1() + line.y2()) / 2
        rect = self.label.boundingRect()
        self.label.setPos(
            mid_x - rect.width() / 2, mid_y - rect.height() / 2)

    def init_pen(self) -> QPen:
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("grey"))
        pen.setStyle(Qt.PenStyle.DashLine)

        return pen
