import json
import shutil
import requests
import subprocess
from io import StringIO
from os import path
from sys import platform
from tempfile import NamedTemporaryFile
from tqdm import tqdm

import PySide6.QtCore as qtc

TITLE = 0
FORMAT = 1
SIZE = 2
PROGRESS = 3
STATUS = 4
SPEED = 5
ETA = 6

V_FORMATS = {
    "mp4": {"video_codec": "h264", "audio": "aac"},
    "webm": {"video_codec": "vp9", "audio": "opus"},
    "mkv": {"video_codec": "h264", "audio": "aac"},
    "avi": {"video_codec": "mpeg4", "audio": "mp3"},
    "flv": {"video_codec": "flv1", "audio": "mp3"},
    "mov": {"video_codec": "h264", "audio": "aac"},
}

V_FORMATS_SUPPORTING_THUMBNAILS = ["mp4", "mkv", "mov"]

A_FORMATS = {
    "mp3": {"codec": "mp3", "max_bitrate_kbps": 320},
    "aac": {"codec": "aac", "max_bitrate_kbps": 512},
    "opus": {"codec": "opus", "max_bitrate_kbps": 510},
    "flac": {"codec": "flac", "max_bitrate_kbps": "lossless"},
    "m4a": {"codec": "aac", "max_bitrate_kbps": 512},
    "wav": {"codec": "pcm_s16le", "max_bitrate_kbps": "lossless"},
    "ogg": {"codec": "vorbis", "max_bitrate_kbps": 500},
    "webm": {"codec": "opus", "max_bitrate_kbps": 510},
}

A_FORMATS_SUPPORTING_THUMBNAILS = ["mp3", "aac", "flac", "m4a"]


class DownloadThread(qtc.QThread):
    progress = qtc.Signal(int, str)

    def __init__(self, url: str, filename: str):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        if not self.filename:
            self.filename = path.basename(self.url)

        request = requests.get(self.url, stream=True)

        total_size = int(request.headers.get("content-length", 0))
        scaling_factor = 100 / total_size
        block_size = 1024
        data = StringIO()
        progress = 0

        with NamedTemporaryFile(mode="wb", delete=False) as temp_file, tqdm(
            desc=path.basename(self.filename),
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            file=data,
            bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}/{remaining}, {rate_fmt}{postfix}]",
            leave=True,
        ) as progress_bar:
            for chunk in request.iter_content(chunk_size=block_size):
                temp_file.write(chunk)
                progress_bar.update(block_size)
                progress += block_size
                self.progress.emit(
                    progress * scaling_factor, data.getvalue().split("\r")[-1].strip()
                )

            temp_file.flush()
            temp_file.close()
        shutil.move(temp_file.name, self.filename)


class ItemSignal(qtc.QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

        - finished = qtc.Signal(int)
        - progress = qtc.Signal(object, list)
    """

    finished = qtc.Signal(int)
    progress = qtc.Signal(object, tuple)


class ItemWorker(qtc.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    """

    def __init__(
        self,
        item,
        url: str,
        path: str,
        filename: str,
        type: str,
        subtitles: bool,
        sublangs: str,
        qvideo: str,
        fvideo: str,
        qaudio: str,
        faudio: str,
        metadata: bool,
        thumbnail: bool,
        noplaylist: bool,
    ) -> None:
        super(ItemWorker, self).__init__()
        self.signals = ItemSignal()

        self.item = item
        self.url = url
        self.path = path
        self.filename = filename
        self.type = type
        self.subtitles = subtitles
        self.sublangs = sublangs
        self.qvideo = qvideo
        self.fvideo = fvideo
        self.qaudio = qaudio
        self.faudio = faudio
        self.metadata = metadata
        self.thumbnail = thumbnail
        self.noplaylist = noplaylist

        self.mutex = qtc.QMutex()
        self._stop = False

    def __str__(self) -> str:
        s = (
            f"(url={self.url}, "
            f"path={self.path}, "
            f"filename={self.filename}, "
            f"type={self.type}, "
            f"subtitles={self.subtitles}, "
            f"sublangs={self.sublangs}, "
            f"qvideo={self.qvideo}, "
            f"fvideo={self.fvideo}, "
            f"qaudio={self.qaudio}, "
            f"faudio={self.faudio}, "
            f"metadata={self.metadata}, "
            f"thumbnail={self.thumbnail}, "
            f"noplaylist={self.noplaylist})"
        )
        return s

    def build_command(self):
        args = [
            "yt-dlp",
            "--newline",
            "--ignore-errors",
            "--ignore-config",
            "--hls-prefer-native",
            "--no-simulate",
            "--progress",
            "--progress-template",
            "%(progress.status)s %(progress._total_bytes_estimate_str)s "
            "%(progress._percent_str)s %(progress._speed_str)s %(progress._eta_str)s",
            "--dump-json",
            "-v",
            "-o",
            f"{self.path}/{self.filename}",
            self.url,
        ]

        if self.type == "Video":
            if self.qvideo == "Best":
                args.extend(["-f", "bestvideo+bestaudio/best"])

            elif self.qvideo == "Worst":
                args.extend(["-f", "worstvideo+worstaudio/worst"])

            else:
                args.extend(
                    [
                        "-f",
                        f"bv*[height<={self.qvideo[:-1]}]+ba/b[height<={self.qvideo[:-1]}]",
                    ]
                )

            args.extend(["--recode-video", self.fvideo])

        elif self.type == "Audio":
            if self.qaudio == "Best":
                args.extend(["-f", "bestaudio"])

            elif self.qaudio == "Worst":
                args.extend(["-f", "worstaudio"])

            else:
                args.extend(["-f", "bestaudio", "--audio-quality", self.qaudio])

            args.extend(["--extract-audio", "--audio-format", self.faudio])

        if self.subtitles:
            args.extend(["--write-sub", "--sub-lang", ",".join(self.sublangs)])

        if self.thumbnail:
            args.append("--embed-thumbnail")

        if self.metadata:
            args.append("--add-metadata")

        if self.noplaylist:
            args.append("--no-playlist")

        return args

    def stop(self):
        with qtc.QMutexLocker(self.mutex):
            self._stop = True

    @qtc.Slot()
    def run(self) -> None:
        """
        Initialise the runner function.
        """
        create_window = subprocess.CREATE_NO_WINDOW if platform == "win32" else 0
        command = self.build_command()
        error = False
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True,
            creationflags=create_window,
        ) as proc:
            for line in proc.stdout:  # type: ignore
                with qtc.QMutexLocker(self.mutex):
                    if self._stop:
                        proc.terminate()
                        break

                if line.startswith("{"):
                    title = json.loads(line)["title"]
                    self.signals.progress.emit(
                        self.item, ((TITLE, title), (STATUS, "Processing"))
                    )

                elif line.lower().startswith("downloading"):
                    data = line.split()
                    self.signals.progress.emit(
                        self.item,
                        (
                            (SIZE, data[1]),
                            (PROGRESS, data[2]),
                            (SPEED, data[3]),
                            (ETA, data[4]),
                            (STATUS, "Downloading"),
                        ),
                    )

                elif line.lower().startswith("error"):
                    error = True
                    self.signals.progress.emit(
                        self.item,
                        (
                            (SIZE, "ERROR"),
                            (STATUS, "ERROR"),
                            (SPEED, "ERROR"),
                        ),
                    )
                    break
                elif line.startswith(("[Merger]", "[ExtractAudio]")):
                    self.signals.progress.emit(
                        self.item,
                        ((STATUS, "Converting"),),
                    )

            if not error:
                self.signals.progress.emit(
                    self.item,
                    (
                        (PROGRESS, "100%"),
                        (STATUS, "Finished"),
                    ),
                )

        self.signals.finished.emit(self.item.id)
