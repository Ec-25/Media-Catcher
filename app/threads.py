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

# Constants for readability and maintainability
TITLE, FORMAT, SIZE, PROGRESS, STATUS, SPEED, ETA = range(7)

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
        self.filename = filename or path.basename(self.url)

    def run(self):
        request = requests.get(self.url, stream=True)
        total_size = int(request.headers.get("content-length", 0))
        scaling_factor = 100 / total_size if total_size > 0 else 1
        block_size = 1024
        data = StringIO()

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
                progress_bar.update(len(chunk))
                self.progress.emit(
                    int(progress_bar.n * scaling_factor),
                    data.getvalue().split("\r")[-1].strip(),
                )

        shutil.move(temp_file.name, self.filename)


class ItemSignal(qtc.QObject):
    """Signals available from a running worker thread."""

    finished = qtc.Signal(int)
    progress = qtc.Signal(object, tuple)


class ItemWorker(qtc.QRunnable):
    def __init__(
        self,
        item,
        url,
        path,
        filename,
        type_,
        subtitles,
        sublangs,
        qvideo,
        fvideo,
        qaudio,
        faudio,
        metadata,
        thumbnail,
        noplaylist,
    ):
        super().__init__()
        self.signals = ItemSignal()

        self.item = item
        self.url = url
        self.path = path
        self.filename = filename
        self.type = type_
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

    def build_command(self):
        """Build the yt-dlp command."""
        args = [
            "yt-dlp",
            "--newline",
            "--ignore-errors",
            "--ignore-config",
            "--hls-prefer-native",
            "--no-simulate",
            "--progress",
            "--progress-template",
            "%(progress.status)s %(progress._total_bytes_estimate_str)s %(progress._percent_str)s %(progress._speed_str)s %(progress._eta_str)s",
            "--dump-json",
            "-v",
            "-o",
            f"{self.path}/{self.filename}",
            self.url,
        ]

        # Video settings
        if self.type == "Video":
            quality_map = {
                "Best": "bestvideo+bestaudio/best",
                "Worst": "worstvideo+worstaudio/worst",
            }
            args.extend(
                [
                    "-f",
                    quality_map.get(
                        self.qvideo,
                        f"bv*[height<={self.qvideo[:-1]}]+ba/b[height<={self.qvideo[:-1]}]",
                    ),
                ]
            )
            args.extend(["--recode-video", self.fvideo])

        # Audio settings
        elif self.type == "Audio":
            args.extend(
                [
                    "-f",
                    (
                        "bestaudio"
                        if self.qaudio == "Best"
                        else "worstaudio" if self.qaudio == "Worst" else "bestaudio"
                    ),
                    "--audio-quality",
                    self.qaudio,
                ]
            )
            args.extend(["--extract-audio", "--audio-format", self.faudio])

        # Additional options
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
    def run(self):
        """Run the yt-dlp process and track progress."""
        command = self.build_command()
        create_window = subprocess.CREATE_NO_WINDOW if platform == "win32" else 0
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
                    if len(data) >= 5:
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
                        ((SIZE, "ERROR"), (STATUS, "ERROR"), (SPEED, "ERROR")),
                    )
                    break

                elif line.startswith(("[Merger]", "[ExtractAudio]")):
                    self.signals.progress.emit(self.item, ((STATUS, "Converting"),))

            if not error:
                self.signals.progress.emit(
                    self.item, ((PROGRESS, "100%"), (STATUS, "Finished"))
                )

        self.signals.finished.emit(self.item.id)
