"""
Main application file.
"""

from PySide6 import QtWidgets, QtCore

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

        ##################################################
        # Widgets.
        ##################################################

        self.le_youtube_link = None
        self.le_album = None
        self.le_artist = None
        self.le_disc_number = None
        self.le_total_discs = None
        self.le_track_number = None
        self.le_total_tracks = None
        self.le_track_title = None
        self.le_year = None
        self.btn_download = None
        self.lbl_drop_info = None
        self.lbl_album_cover = None

        self.ui_manage_widgets()

        ##################################################
        # Icons.
        ##################################################

        self.ui_manage_icons()

    def ui_manage_icons(self) -> None:
        """Icons are managed here."""

        self.setWindowIcon(self.icons.get("logo"))
        self.lbl_album_cover.setPixmap(self.icons.get("drop_cover"))

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here."""

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.setContentsMargins(20, 20, 10, 20)
        self.right_layout = QtWidgets.QGridLayout()
        self.right_layout.setContentsMargins(10, 0, 20, 0)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here."""

        self.le_youtube_link = QtWidgets.QLineEdit()
        self.le_youtube_link.setPlaceholderText("Paste YouTube link here.")
        self.le_album = QtWidgets.QLineEdit()
        self.le_album.setPlaceholderText("Album")
        self.le_artist = QtWidgets.QLineEdit()
        self.le_artist.setPlaceholderText("Artist")
        self.le_disc_number = QtWidgets.QLineEdit()
        self.le_disc_number.setPlaceholderText("Disc Number")
        self.le_total_discs = QtWidgets.QLineEdit()
        self.le_total_discs.setPlaceholderText("Total Discs")
        self.le_track_number = QtWidgets.QLineEdit()
        self.le_track_number.setPlaceholderText("Track Number")
        self.le_total_tracks = QtWidgets.QLineEdit()
        self.le_total_tracks.setPlaceholderText("Total Tracks")
        self.le_track_title = QtWidgets.QLineEdit()
        self.le_track_title.setPlaceholderText("Track Title")
        self.le_year = QtWidgets.QLineEdit()
        self.le_year.setPlaceholderText("Year")
        self.btn_download = QtWidgets.QPushButton("Download")
        self.lbl_drop_info = QtWidgets.QLabel("Drop the album cover below.")
        self.lbl_drop_info.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.lbl_album_cover = QtWidgets.QLabel()
        self.lbl_album_cover.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore

        self.left_layout.addWidget(self.le_youtube_link)
        self.left_layout.addWidget(self.btn_download)
        self.left_layout.addWidget(self.lbl_drop_info)
        self.left_layout.addWidget(self.lbl_album_cover)
        self.right_layout.addWidget(self.le_album, 0, 0)
        self.right_layout.addWidget(self.le_artist, 0, 1)
        self.right_layout.addWidget(self.le_disc_number, 1, 0)
        self.right_layout.addWidget(self.le_total_discs, 1, 1)
        self.right_layout.addWidget(self.le_track_number, 2, 0)
        self.right_layout.addWidget(self.le_total_tracks, 2, 1)
        self.right_layout.addWidget(self.le_track_title, 3, 0)
        self.right_layout.addWidget(self.le_year, 3, 1)


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
