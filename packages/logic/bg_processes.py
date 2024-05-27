"""
This module provides the DownloadAndProcess class, which is a QThread subclass
for downloading audio from a YouTube video, converting it to MP3 format, and
tagging it with user information in the background.
"""

from pathlib import Path

from PySide6.QtCore import QThread, Signal
from pytube import YouTube
from pydub import AudioSegment


class DownloadAndProcess(QThread):

    download_finished = Signal()
    file_converted = Signal()
    error_happened = Signal()

    def __init__(self):
        super().__init__()

        self.output_directory: Path = Path.home() / "Downloads"
        self._youtube_link = None
        self.output_directory.mkdir(exist_ok=True, parents=True)

    def convert_file(self, file: Path) -> Path:
        """Converts the downloaded audio file to MP3 format.

        Args:
            file (Path): The path to the downloaded audio file.

        Returns:
            Path: The path to the converted MP3 file.
        """

        try:

            mp3_file = file.with_suffix('.mp3')
            audio = AudioSegment.from_file(file)
            audio.export(mp3_file, format="mp3", bitrate="192k")

        except Exception as error:

            print(f"Error during conversion: {error}")
            self.error_happened.emit()
            return Path("")

        else:

            self.file_converted.emit()
            return mp3_file

    def download_file(self) -> Path:
        """Downloads the audio from the YouTube video.

        Returns:
            Path: The path to the downloaded audio file.
        """

        try:

            target = YouTube(self._youtube_link)
            audio_stream = target.streams.filter(only_audio=True).first()
            audio_file = Path(audio_stream.download(output_path=self.output_directory))

        except Exception as error:

            print(f"Error during download: {error}")
            self.error_happened.emit()
            return Path("")

        else:

            self.download_finished.emit()
            return audio_file

    def run(self) -> None:

        file: Path = self.download_file()
        mp3_file: Path = self.convert_file(file=file)

        if file.exists() and file.is_file():
            file.unlink()

    def set_url(self, link: str) -> None:
        """Sets the YouTube video URL to download and convert.

        Args:
            link (str): The YouTube video URL.
        """

        self._youtube_link = link
