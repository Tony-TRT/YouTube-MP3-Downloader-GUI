"""
Main application file.
"""

from PySide6 import QtWidgets

from packages.ui.aesthetic import AestheticWindow


class MainWindow(AestheticWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("YouTube MP3 Downloader")
        self.setFixedSize(900, 500)

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None
        self.left_layout = None
        self.right_layout = None

        self.ui_manage_layouts()

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here."""

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QGridLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
