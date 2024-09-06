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


class ItemThread(qtc.QThread):
    finished = qtc.Signal(int)
    progress = qtc.Signal(object, list)

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
        super().__init__()
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
            if self.qvideo:
                try:
                    int(self.qvideo[:-1])
                    args.extend(
                        ["-f", f"bestvideo[height<={self.qvideo[:-1]}]+bestaudio/best"]
                    )
                except ValueError:
                    if self.qvideo.lower() == "best":
                        args.extend(["-f", "bestvideo+bestaudio/best"])
                    elif self.qvideo.lower() == "worst":
                        args.extend(["-f", "worstvideo+worstaudio/worst"])
                    else:
                        raise ValueError(f"Valor no válido para qvideo: {self.qvideo}")

            if self.fvideo:
                args.extend(["--merge-output-format", self.fvideo])

            if self.subtitles:
                args.extend(["--write-sub", "--sub-lang", ",".join(self.sublangs)])

        elif self.type == "Audio":
            if self.qaudio:
                try:
                    int(self.qaudio[:-1])
                    args.extend(["-f", f"bestaudio[abr<={self.qaudio[:-1]}]"])
                except ValueError:
                    if self.qaudio.lower() == "best":
                        args.extend(["-f", "bestaudio"])
                    elif self.qaudio.lower() == "worst":
                        args.extend(["-f", "worstaudio"])
                    else:
                        raise ValueError(f"Valor no válido para qaudio: {self.qaudio}")

            if self.faudio:
                args.extend(["--audio-format", self.faudio])
            args.extend(["--extract-audio"])

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

    def run(self) -> None:
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
                print(line)
                with qtc.QMutexLocker(self.mutex):
                    if self._stop:
                        proc.terminate()
                        break

                if line.startswith("{"):
                    title = json.loads(line)["title"]
                    self.progress.emit(
                        self.item,
                        [(TITLE, title), (STATUS, "Processing")],
                    )
                elif line.lower().startswith("downloading"):
                    data = line.split()
                    self.progress.emit(
                        self.item,
                        [
                            (SIZE, data[1]),
                            (PROGRESS, data[2]),
                            (SPEED, data[3]),
                            (ETA, data[4]),
                            (STATUS, "Downloading"),
                        ],
                    )
                elif line.lower().startswith("error"):
                    error = True
                    self.progress.emit(
                        self.item,
                        [
                            (SIZE, "ERROR"),
                            (STATUS, "ERROR"),
                            (SPEED, "ERROR"),
                        ],
                    )
                    break
                elif line.startswith(("[Merger]", "[ExtractAudio]")):
                    self.progress.emit(self.item, [(STATUS, "Converting")])

            if not error:
                self.progress.emit(
                    self.item,
                    [
                        (PROGRESS, "100%"),
                        (STATUS, "Finished"),
                    ],
                )

        self.finished.emit(self.item.id)
