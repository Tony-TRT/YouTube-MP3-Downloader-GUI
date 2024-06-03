"""
This module contains custom widgets.
"""

from PySide6 import QtCore
from PySide6.QtWidgets import QLineEdit, QLabel, QProgressBar
from PySide6.QtGui import Qt, QPainter, QPen, QColor


class CustomQLineEdit(QLineEdit):
    """
    A custom QLineEdit widget with a fixed size.

    This widget inherits from QLineEdit and sets a fixed size of 215x40 pixels.
    Each instance of this class is stored in the class-level `instances` dictionary,
    with the placeholder text as the key.
    """

    instances: dict = {}

    def __init__(self, parent=None, placeholder_text: str = None):
        super().__init__(parent=parent)

        self.setFixedSize(215, 40)

        if placeholder_text and isinstance(placeholder_text, str):
            self.setPlaceholderText(placeholder_text)
            CustomQLineEdit.instances[placeholder_text] = self


class CustomQLabel(QLabel):
    """A customized QLabel class for creating labels with specific styles and properties."""

    def __init__(self, parent=None, size: tuple[int, int] = None, text: str = None):
        super().__init__(parent=parent)

        if text:
            self.setText(text)

        if size:
            self.setFixedSize(*size)

        self.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.setStyleSheet("color: #000000; background: #87A9B5; border-radius: 15px;")


class CustomQProgressBar(QProgressBar):
    """
    Customized QProgressBar with a non-rectangular progress indicator.

    This class extends the functionality of QProgressBar to render a progress bar with a custom shape.
    The progress indicator follows a non-rectangular path specified by a list of points.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setValue(0)
        self.setGeometry(QtCore.QRect(0, 55, 900, 105))

    def paintEvent(self, arg__1):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # type: ignore

        # Define the path points for the progress indicator
        path_points: list[tuple] = [
            (0, 103, 448, 103),
            (448, 103, 448, 3),
            (448, 3, 900, 3)
        ]

        # Calculate the total length of the path
        total_length: int = sum([abs(x2 - x1) + abs(y2 - y1) for x1, y1, x2, y2 in path_points])

        # Calculate the length of progress based on the current value
        progress_length: int = int((self.value() / self.maximum()) * total_length)

        # Define the pen for drawing the progress indicator
        progress_pen = QPen(QColor("#FFA500"), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  # type: ignore
        painter.setPen(progress_pen)
        current_length: int = 0

        # Iterate through each segment of the path and draw the progress indicator
        for x1, y1, x2, y2 in path_points:

            segment_length: int = abs(x2 - x1) + abs(y2 - y1)

            if progress_length <= current_length + segment_length:

                # Draw the portion of the progress indicator within the current segment
                if x1 == x2:
                    painter.drawLine(x1, y1, x1, y1 + (progress_length - current_length) * (1 if y2 > y1 else -1))

                else:
                    painter.drawLine(x1, y1, x1 + (progress_length - current_length) * (1 if x2 > x1 else -1), y1)
                break

            else:
                # Draw the entire segment
                painter.drawLine(x1, y1, x2, y2)
                current_length += segment_length
