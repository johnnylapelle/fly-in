from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem

from ..zone import Zone
from .utils import RADIUS, SCALE


class ZoneItem(QGraphicsEllipseItem):
    def __init__(self, zone: Zone) -> None:
        super().__init__(
             -RADIUS / 2, -RADIUS / 2, RADIUS, RADIUS)

        self.zone = zone
        self.setPos(zone.x * SCALE, zone.y * SCALE)
        self.setBrush(QBrush(QColor(zone.color)))
        self.setPen(QPen(QColor(zone.color)))
