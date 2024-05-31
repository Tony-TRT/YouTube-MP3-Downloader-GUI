"""
Main application file.
"""

from functools import partial

from PySide6 import QtWidgets

from packages.ui.aesthetic import AestheticWindow
from packages.logic import toolkit, bg_processes


class MainWindow(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube MP3 Downloader")
        self.setFixedSize(900, 500)
        self.setAcceptDrops(True)
        self.current_cover = None
        self.metadata: dict = {
            "album": None,
            "artist": None,
            "discnumber": None,
            "tracknumber": None,
            "title": None,
            "date": None,
            "cover": None
        }
        self.thread = bg_processes.DownloadAndProcess()

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
        # Graphics.
        ##################################################

        self.ui_manage_graphics()

        ##################################################
        # Connections.
        ##################################################

        self.logic_connect_widgets()

    def dragEnterEvent(self, event):

        event.accept()

    def dropEvent(self, event):
        """Handle file drop events, process image files, and update the album cover label."""

        event.accept()
        dropped_file = event.mimeData().urls()[0].toLocalFile()

        if dropped_file.split('.')[-1].casefold() in ['jpg', 'jpeg', 'png', 'bmp']:

            self.current_cover = toolkit.process_album_cover(image=dropped_file)
            self.lbl_album_cover.setPixmap(self.current_cover[0])

    def ui_manage_graphics(self) -> None:
        """Graphics are managed here."""

        self.setWindowIcon(self.images.get("logo"))
        self.lbl_album_cover.setPixmap(self.images.get("drop_cover"))

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
        self.lbl_album_cover = QtWidgets.QLabel()

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

    def logic_connect_widgets(self) -> None:
        """Connections are managed here."""

        self.btn_download.clicked.connect(self.logic_main_process)
        self.thread.download_finished.connect(partial(self.logic_display_progress, 1))
        self.thread.file_converted.connect(partial(self.logic_display_progress, 2))
        self.thread.file_tagged.connect(partial(self.logic_display_progress, 3))
        self.thread.error_happened.connect(partial(self.logic_display_progress, -1))

    def logic_display_progress(self, step: int) -> None:
        """Update the window title to display overall progress.

        Args:
            step (int): The current step of the overall process.
        """

        step_map: dict = {
            -1: " - An error has occurred.",
            0: " - Downloading...",
            1: " - Converting...",
            2: " - Writing metadata...",
            3: " - Success!"
        }

        self.setWindowTitle("YouTube MP3 Downloader" + step_map.get(step, ""))

    def logic_error_dialog(self, message: str) -> None:
        """Display a critical error dialog with the given message.

        Args:
            message (str): The error message to display in the dialog.
        """

        QtWidgets.QMessageBox.critical(self, "Error", message)

    def logic_main_process(self) -> None:
        """Processes the information entered by the user and attempts to create the desired mp3 file."""

        youtube_link: str = self.le_youtube_link.text()

        if not toolkit.check_link(text=youtube_link):
            error_message: str = "The provided link is not a valid YouTube link."
            self.logic_error_dialog(message=error_message)
            return

        strings: list[str] = [
            QLineEdit.text() for QLineEdit in {
                self.le_disc_number,
                self.le_total_discs,
                self.le_track_number,
                self.le_total_tracks,
                self.le_year
            }
        ]

        if not toolkit.check_data(strings=strings):
            error_message: str = "At least one of the provided tags is not a numeric value, although it should be."
            self.logic_error_dialog(message=error_message)
            return

        self.metadata["album"] = self.le_album.text()
        self.metadata["artist"] = self.le_artist.text()
        self.metadata["discnumber"] = f"{self.le_disc_number.text()}/{self.le_total_discs.text()}"
        self.metadata["tracknumber"] = f"{self.le_track_number.text()}/{self.le_total_tracks.text()}"
        self.metadata["title"] = self.le_track_title.text()
        self.metadata["date"] = self.le_year.text()
        self.metadata["cover"] = self.current_cover[1] if self.current_cover else None

        self.logic_display_progress(0)
        self.thread.set_url(link=youtube_link)
        self.thread.set_metadata(metadata=self.metadata)
        self.thread.start()


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
