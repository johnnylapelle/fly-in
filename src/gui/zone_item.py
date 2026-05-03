from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem

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

        info = (f"{zone.name}\n{zone.zone_type}\n"
                f"{zone.max_drones} drones\n({zone.x}, {zone.y})")
        self.label = QGraphicsTextItem(info, self)
        self.label.setPos(-RADIUS / 2, RADIUS / 2)

    def toggle_label(self) -> None:
        self.label.setVisible(not self.label.isVisible())
