from typing import Callable

from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import (QGraphicsEllipseItem, QGraphicsSceneMouseEvent,
                             QGraphicsTextItem)

from ..core.zone import Zone
from .utils import RADIUS, SCALE


class ZoneItem(QGraphicsEllipseItem):
    def __init__(self,
                 zone: Zone, on_click: Callable[['ZoneItem'], None]) -> None:
        QGraphicsEllipseItem.__init__(
            self, -RADIUS / 2, -RADIUS / 2, RADIUS, RADIUS)

        self._zone = zone
        self.setPos(zone.x * SCALE, zone.y * SCALE)
        self.setBrush(QBrush(QColor(zone.color)))
        self.setPen(QPen(QColor(zone.color)))

        # display zone informations
        self.label = QGraphicsTextItem(self)
        self.label.setTextWidth(200)
        self.label.setHtml(
            f"<center>{self._zone.name}<br>"
            f"{self._zone.type}<br>"
            f"{self._zone.max_drones} drones</center>")
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, rect.height() / 2 + 25)

        self._on_click = on_click

    def toggle_label(self) -> None:
        self.label.setVisible(not self.label.isVisible())

    def set_label_visible(self, on_off: bool) -> None:
        self.label.setVisible(on_off)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self._on_click(self)
        return super().mousePressEvent(event)
