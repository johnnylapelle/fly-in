from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class OverlayPanel(QWidget):
    load_map_requested = pyqtSignal()
    toggle_desc_requested = pyqtSignal()
    reset_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._btn_load_map = QPushButton('Load Map (M)')
        self._btn_toggle_desc = QPushButton('Hide Description (H)')
        self._btn_reset = QPushButton('Reset (R)')

        for btn in (self._btn_load_map,
                    self._btn_toggle_desc,
                    self._btn_reset):
            layout.addWidget(btn)

        self._btn_load_map.clicked.connect(self.load_map_requested)
        self._btn_toggle_desc.clicked.connect(self.toggle_desc_requested)
        self._btn_reset.clicked.connect(self.reset_requested)

    def set_text_description(self, visible: bool) -> None:
        self._btn_toggle_desc.setText(
            'Hide Description (H)' if visible else 'Show Description (H)'
        )
