"""
This module provides the DownloadAndProcess class, which is a QThread subclass
for downloading audio from a YouTube video, converting it to MP3 format, and
tagging it with user information in the background.
"""

from pathlib import Path
from time import sleep

import pytube
from PySide6.QtCore import QThread, Signal
from pydub import AudioSegment
from mutagen import id3

from packages.constants import constants
from packages.logic.toolkit import qthread_error_handler


class DownloadAndProcess(QThread):

    download_finished = Signal()
    file_converted = Signal()
    file_tagged = Signal()
    error_happened = Signal()

    def __init__(self):
        super().__init__()

        self.output_directory: Path = Path.home() / "Downloads"
        self.output_directory.mkdir(exist_ok=True, parents=True)
        self.youtube_link = None
        self.metadata = None
        self.quality = None

    @qthread_error_handler
    def convert_file(self, file: Path) -> Path:
        """Converts the downloaded audio file to MP3 format.

        Args:
            file (Path): The path to the downloaded audio file.

        Returns:
            Path: The path to the converted MP3 file.
        """

        mp3_file: Path = file.with_suffix('.mp3')
        audio = AudioSegment.from_file(file)
        audio.export(mp3_file, format="mp3", bitrate=self.quality)
        self.file_converted.emit()
        sleep(0.7)  # Delay to allow the progress to be seen
        return mp3_file

    @qthread_error_handler
    def download_file(self) -> Path:
        """Downloads the audio from the YouTube video.

        Returns:
            Path: The path to the downloaded audio file.
        """

        target: pytube.YouTube = pytube.YouTube(self.youtube_link)
        audio_stream = target.streams.filter(only_audio=True).first()
        audio_file: Path = Path(audio_stream.download(output_path=self.output_directory))
        self.download_finished.emit()
        return audio_file

    @qthread_error_handler
    def tag_file(self, file: Path) -> None:
        """Tags the given MP3 file with metadata and cover image if available.

        Args:
            file (Path): The path to the MP3 file to be tagged.
        """

        metadata = id3.ID3(file)
        cover: bytes | None = self.metadata.popitem()[1]

        metadata.add(id3.TIT2(encoding=3, text=self.metadata.get("title")))
        metadata.add(id3.TPE1(encoding=3, text=self.metadata.get("artist")))
        metadata.add(id3.TALB(encoding=3, text=self.metadata.get("album")))
        metadata.add(id3.TDRC(encoding=3, text=self.metadata.get("year")))
        metadata.add(id3.TCON(encoding=3, text=self.metadata.get("genre")))
        metadata.add(id3.TCOP(encoding=3, text=self.metadata.get("copyright")))
        metadata.add(id3.TPOS(encoding=3, text=self.metadata.get("disc_number")))
        metadata.add(id3.TRCK(encoding=3, text=self.metadata.get("track_number")))

        if cover:
            apic = id3.APIC(encoding=3, mime="image/png", type=3, desc=u"Cover", data=cover)
            metadata.delall("APIC")
            metadata.add(apic)

        metadata.save()
        self.file_tagged.emit()

    def run(self) -> None:

        file: Path = self.download_file()
        mp3_file: Path = self.convert_file(file=file)

        if isinstance(file, Path) and file.is_file():
            file.unlink()

        self.tag_file(file=mp3_file)
        data: bool = self.metadata.get("artist") and self.metadata.get("title")
        filename: str = f"{self.metadata["artist"]} - {self.metadata["title"]}.mp3" if data else ""

        if filename:
            mp3_file.rename(Path.joinpath(mp3_file.parent, filename))


class DetectVideoCopyright(QThread):

    this_is_ok_signal = Signal()
    this_is_not_ok_signal = Signal()
    composers = set()

    def __init__(self):
        super().__init__()

        self.youtube_url = None
        self.video_title = None
        self.load_composers()

    @classmethod
    def load_composers(cls) -> None:
        """Load composers from the file specified in constants.COMPOSERS."""

        with open(constants.COMPOSERS, "r", encoding="UTF-8") as file:
            cls.composers = {line.strip().lower() for line in file}

    def run(self) -> None:

        if not self.youtube_url:
            return

        try:
            self.video_title: str = pytube.YouTube(self.youtube_url).streams[0].title

        except pytube.exceptions.RegexMatchError:  # type: ignore
            return

        if not (self.video_title and isinstance(self.video_title, str)):
            self.this_is_not_ok_signal.emit()
            return

        if any(composer in self.video_title.lower() for composer in self.composers):
            self.this_is_ok_signal.emit()

        else:
            self.this_is_not_ok_signal.emit()
