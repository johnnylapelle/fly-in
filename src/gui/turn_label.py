from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TurnLabel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._turn_label = QLabel()
        self._turn_label.setText('Map: test  Turn: 0  Drones: 0')
        self._turn_label.setStyleSheet('''
                font-size: 20px;
                color: black;''')
        self._turn_label.adjustSize()

        layout.addWidget(self._turn_label)

    def setText(self, text: str) -> None:
        self._turn_label.setText(text)
