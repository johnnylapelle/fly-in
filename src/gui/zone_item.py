from typing import Callable

from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import (QGraphicsEllipseItem, QGraphicsSceneMouseEvent,
                             QGraphicsTextItem)

from ..zone import Zone
from .utils import RADIUS, SCALE


class ZoneItem(QGraphicsEllipseItem):
    def __init__(self, zone: Zone, on_click: Callable) -> None:
        QGraphicsEllipseItem.__init__(self,
             -RADIUS / 2, -RADIUS / 2, RADIUS, RADIUS)

        self._zone = zone
        self.setPos(zone.x * SCALE, zone.y * SCALE)
        self.setBrush(QBrush(QColor(zone.color)))
        self.setPen(QPen(QColor(zone.color)))

        info = (f"{zone.name}\n{zone.zone_type}\n"
                f"{zone.max_drones} drones\n({zone.x}, {zone.y})")
        self.label = QGraphicsTextItem(info, self)
        self.label.setPos(-RADIUS / 2, RADIUS / 2)

        self._on_click = on_click

    def toggle_label(self) -> None:
        self.label.setVisible(not self.label.isVisible())

    def set_label_visible(self, on_off: bool) -> None:
        self.label.setVisible(on_off)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self._on_click(self)
        super().mousePressEvent(event)
