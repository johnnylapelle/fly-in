from typing import Callable

from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import (QGraphicsEllipseItem, QGraphicsSceneMouseEvent,
                             QGraphicsTextItem)
from PyQt6.QtCore import QTimer

from ..core.zone import Zone
from .utils import RADIUS, SCALE, get_color


class ZoneItem(QGraphicsEllipseItem):
    def __init__(self,
                 zone: Zone, on_click: Callable[['ZoneItem'], None]) -> None:
        QGraphicsEllipseItem.__init__(
            self, -RADIUS / 2, -RADIUS / 2, RADIUS, RADIUS)

        self._zone = zone
        self.setPos(zone.x * SCALE, zone.y * SCALE)

        if zone.color == "rainbow":
            self.hue = 0
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_color)
            self.timer.start(30)
        else:
            pen = QPen(QColor(get_color(zone.color)))
            pen.setWidth(3)

            brush = QBrush(QColor(get_color(zone.color)))

            self.setPen(pen)
            self.setBrush(brush)

        # display zone informations
        self.label = QGraphicsTextItem(self)
        self.label.setTextWidth(200)
        self.label.setHtml(
            f"<center>{self._zone.name}<br>"
            f"{self._zone.type}<br>"
            f"{self._zone.max_drones} drones</center>")
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, rect.height() / 2 + 25)
        self.label.setDefaultTextColor(QColor("black"))

        self._on_click = on_click

    def toggle_label(self) -> None:
        self.label.setVisible(not self.label.isVisible())

    def set_label_visible(self, on_off: bool) -> None:
        self.label.setVisible(on_off)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self._on_click(self)
        return super().mousePressEvent(event)

    def update_color(self) -> None:
        color = QColor.fromHsv(self.hue, 255, 255)

        self.setBrush(QBrush(color))
        self.setPen(QPen(color))

        self.hue = (self.hue + 2) % 360
