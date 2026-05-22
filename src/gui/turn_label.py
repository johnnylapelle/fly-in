from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TurnLabel(QWidget):
    """
    Displays the current map name, turn number, and drone count.

    Rendered as an overlay in the top-right corner of the main window.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Args:
            parent: Parent widget. Pass the main window to render
                the label as an overlay.
        """

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
        """
        Updates the displayed text.

        Args:
            text: The new text to display.
        """

        self._turn_label.setText(text)
