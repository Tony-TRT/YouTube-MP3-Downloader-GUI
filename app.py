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


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
