from .utils import get_style
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QStyle
from ..simulation.simulation_state import SimulationState


class SimControls(QWidget):
    prev_requested = pyqtSignal()
    play_requested = pyqtSignal()
    next_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn_prev = QPushButton()
        self._btn_play = QPushButton()
        self._btn_next = QPushButton()

        for btn in (self._btn_prev, self._btn_play, self._btn_next):
            layout.addWidget(btn)

        self._btn_prev.clicked.connect(self.prev_requested)
        self._btn_play.clicked.connect(self.play_requested)
        self._btn_next.clicked.connect(self.next_requested)

        self._set_icons()

    def _set_icons(self) -> None:
        style = get_style()

        self._btn_prev.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self._btn_play.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self._btn_next.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))

    def set_playing(self, state: SimulationState) -> None:
        if state == SimulationState.RUNNING:
            pixmap = (QStyle.StandardPixmap.SP_MediaPause)
        elif state == SimulationState.FINISHED:
            pixmap = (QStyle.StandardPixmap.SP_ArrowBack)
        else:
            pixmap = (QStyle.StandardPixmap.SP_MediaPlay)

        self._btn_play.setIcon(get_style().standardIcon(pixmap))
