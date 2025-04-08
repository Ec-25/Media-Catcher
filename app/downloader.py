from datetime import datetime
from pathlib import Path
import re
import signal
import time
from urllib.parse import urlparse
from requests import get as get_request
import subprocess
import os
import json

from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import QRunnable, QThread, QObject, Signal, QByteArray
from PySide6.QtGui import QPixmap

from gui.config import Ui_Config

from translations import translations


class ConfigWindow(QDialog, Ui_Config):
    save_signal = Signal(dict)
    cancel_signal = Signal()

    def __init__(self, main_window, lang: str, configuration: dict):
        super().__init__()
        self.lang = lang
        self.dictionary = translations[self.lang]
        self.setupUi(self)
        main_window.close_all.connect(self.close)
        self.init_language()
        self.configuration = configuration
        self.set_configuration()
        self.connectEvents()
        self.type_change()
        self.show()

    def reload_language(self, lang: str):
        """Reload the language of the application"""
        # set the language in the application and in the settings
        self.lang = lang
        self.dictionary = translations[lang]

        self.init_language()

    def init_language(self):
        base = self.dictionary["configuration"]
        self.setWindowTitle(base["titleAPP"])
        self.title.setText(base["title"])
        self.lb_path.setText(base["path"])
        self.le_path.setPlaceholderText(base["pathPH"])
        self.pb_path.setToolTip(base["browse"])
        self.lb_filename.setText(base["filename"])
        self.le_filename.setPlaceholderText(base["filenamePH"])
        self.pb_revertFilename.setToolTip(base["revert"])
        self.cb_maxDownloads.setText(base["max_download"])
        self.lb_type.setText(base["type"])
        self.lb_qvideo.setText(base["quality_video"])
        self.cb_qvideo.setItemText(0, base["quality_highest"])
        self.cb_qvideo.setItemText(1, base["quality_worst"])
        self.lb_fvideo.setText(base["format_video"])
        self.lb_qaudio.setText(base["quality_audio"])
        self.cb_qaudio.setItemText(0, base["quality_highest"])
        self.cb_qaudio.setItemText(1, base["quality_worst"])
        self.lb_faudio.setText(base["format_audio"])
        self.cb_subtitles.setText(base["subtitles"])
        self.le_lang_subtitles.setPlaceholderText(base["subtitlesPH"])
        self.le_cookies.setPlaceholderText(base["select_filePH"])
        self.pb_cookies.setToolTip(base["browse"])
        self.cb_limitRate.setText(base["limit_rate"])
        self.le_limitRate.setPlaceholderText(base["limit_ratePH"])
        self.le_proxy.setPlaceholderText(base["proxyPH"])
        self.cb_thumbnail.setText(base["thumbnail"])
        self.cb_noOverwrites.setText(base["no_overwrites"])
        self.cb_metadata.setText(base["metadata"])
        self.cb_embedSubs.setText(base["embed_subtitles"])
        self.cb_restrictFilename.setText(base["restrict_filename"])
        self.cb_noPlaylist.setText(base["no_playlist"])
        self.cb_downloadArchive.setText(base["download_archive"])
        self.pb_save.setText(base["save"])
        self.pb_cancel.setText(base["cancel"])

    def set_configuration(self):
        self.le_path.setText(self.configuration["path"] if self.configuration["path"] != "default" else (
            Path(__file__).parent / "download").__str__())
        self.le_filename.setText(
            self.configuration["filename"] if self.configuration["filename"] != "default" else "%(title)s.%(ext)s")
        self.cb_maxDownloads.setChecked(self.configuration["cb_max_downloads"])
        if self.configuration["cb_max_downloads"]:
            self.sb_maxDownloads.setEnabled(True)
        self.sb_maxDownloads.setValue(int(self.configuration["max_downloads"]))
        self.cb_type.setCurrentIndex(int(self.configuration["type"])),
        match self.configuration["quality_video"]:
            case "Best":
                self.cb_qvideo.setCurrentText(
                    self.dictionary["configuration"]["quality_highest"])
            case "Worst":
                self.cb_qvideo.setCurrentText(
                    self.dictionary["configuration"]["quality_worst"])
            case _:
                self.cb_qvideo.setCurrentText(
                    self.configuration["quality_video"])
        self.cb_fvideo.setCurrentText(self.configuration["format_video"])
        match self.configuration["quality_audio"]:
            case "Best":
                self.cb_qaudio.setCurrentText(
                    self.dictionary["configuration"]["quality_highest"])
            case "Worst":
                self.cb_qaudio.setCurrentText(
                    self.dictionary["configuration"]["quality_worst"])
            case _:
                self.cb_qaudio.setCurrentText(
                    self.configuration["quality_audio"])
        self.cb_faudio.setCurrentText(self.configuration["format_audio"])
        self.cb_subtitles.setChecked(self.configuration["cb_subtitles"])
        if self.configuration["cb_subtitles"]:
            self.le_lang_subtitles.setEnabled(True)
        self.le_lang_subtitles.setText(self.configuration["lang_subtitles"])
        self.cb_cookies.setChecked(self.configuration["cb_cookies"])
        if self.configuration["cb_cookies"]:
            self.le_cookies.setEnabled(True)
            self.pb_cookies.setEnabled(True)
        self.le_cookies.setText(self.configuration["cookies"])
        self.cb_limitRate.setChecked(self.configuration["cb_limit_rate"])
        if self.configuration["cb_limit_rate"]:
            self.le_limitRate.setEnabled(True)
        self.le_limitRate.setText(self.configuration["limit_rate"])
        self.cb_proxy.setChecked(self.configuration["cb_proxy"])
        if self.configuration["cb_proxy"]:
            self.le_proxy.setEnabled(True)
        self.le_proxy.setText(self.configuration["proxy"])
        self.cb_thumbnail.setChecked(self.configuration["cb_thumbnail"])
        self.cb_noOverwrites.setChecked(self.configuration["cb_no_overwrites"])
        self.cb_metadata.setChecked(self.configuration["cb_metadata"])
        self.cb_embedSubs.setChecked(self.configuration["cb_embed_subtitles"])
        self.cb_restrictFilename.setChecked(
            self.configuration["cb_restrict_filename"])
        self.cb_noPlaylist.setChecked(self.configuration["cb_no_playlist"])
        self.cb_downloadArchive.setChecked(
            self.configuration["cb_download_archive"])

    def connectEvents(self):
        self.cb_type.currentIndexChanged.connect(self.type_change)
        self.pb_path.clicked.connect(self.browse_path)
        self.pb_revertFilename.clicked.connect(self.revert_filename)
        self.cb_type.currentIndexChanged.connect(self.format_change)
        self.cb_fvideo.currentIndexChanged.connect(self.format_change)
        self.cb_faudio.currentIndexChanged.connect(self.format_change)
        self.pb_cookies.clicked.connect(self.browse_cookies)
        self.pb_save.clicked.connect(self.save_config)
        self.pb_cancel.clicked.connect(self.cancel)

    def format_change(self):
        type_media = self.cb_type.currentIndex()
        index_video = self.cb_fvideo.currentIndex()
        MAX_V_FORMATS_INDEX_SUPPORTING_THUMBNAILS = 2
        index_audio = self.cb_faudio.currentIndex()
        MAX_A_FORMATS_INDEX_SUPPORTING_THUMBNAILS = 3

        invalid_video = index_video > MAX_V_FORMATS_INDEX_SUPPORTING_THUMBNAILS
        invalid_audio = index_audio > MAX_A_FORMATS_INDEX_SUPPORTING_THUMBNAILS

        if type_media == 0:  # video
            if invalid_video or invalid_audio:
                self.cb_thumbnail.setChecked(False)
                self.cb_thumbnail.setDisabled(True)
            else:
                self.cb_thumbnail.setEnabled(True)
        elif type_media == 1:  # audio
            if invalid_audio:
                self.cb_thumbnail.setChecked(False)
                self.cb_thumbnail.setDisabled(True)
            else:
                self.cb_thumbnail.setEnabled(True)

    def type_change(self):
        id = self.cb_type.currentIndex()
        if id == 0:
            self.cb_fvideo.setEnabled(True)
            self.cb_qvideo.setEnabled(True)
        elif id == 1:
            self.cb_fvideo.setDisabled(True)
            self.cb_qvideo.setDisabled(True)

    def cancel(self):
        self.cancel_signal.emit()
        self.close()

    def save_config(self):
        def is_valid_proxy_format(proxy: str) -> bool:
            pattern = r"^(http|https|socks4|socks5)://[^:@\s]+(:[^@\s]+)?@?[^:\s]+(:\d+)?$"
            return re.match(pattern, proxy) is not None

        def get_limit_rate() -> str:
            text = self.le_limitRate.text()
            limit = float(text[:-1])
            unit = text[-1].lower()
            if unit not in ("k", "m"):
                raise ValueError("limit_rate")
            return f"{limit}{unit.upper()}"

        def validate_proxy():
            proxy = self.le_proxy.text()
            if proxy and not is_valid_proxy_format(proxy):
                raise ValueError("proxy")
            return proxy

        try:
            if self.cb_limitRate.isChecked():
                limit_rate = get_limit_rate()
            else:
                limit_rate = ""
                self.le_limitRate.setText(limit_rate)

            if self.cb_proxy.isChecked():
                proxy = validate_proxy()
            else:
                proxy = ""
                self.le_proxy.setText(proxy)

        except ValueError as e:
            error_key = e.args[0] if e.args else "unknown"
            QMessageBox.critical(self, "Error", self.dictionary["errors"].get(
                error_key, "Unknown error"))
            return

        quality_video = {
            "Mejor Calidad": "Best",
            "Better Quality": "Best",
            "Menor Peso": "Worst",
            "Lower Weight": "Worst"
        }.get(self.cb_qvideo.currentText(), self.cb_qvideo.currentText())

        quality_audio = {
            "Mejor Calidad": "Best",
            "Better Quality": "Best",
            "Menor Peso": "Worst",
            "Lower Weight": "Worst"
        }.get(self.cb_qaudio.currentText(), self.cb_qaudio.currentText())

        default_path = str(Path(__file__).parent / "download")

        conf = {
            "path": self.le_path.text() if self.le_path.text() != default_path else "default",
            "filename": self.le_filename.text() if self.le_filename.text() != "%(title)s.%(ext)s" else "default",
            "cb_max_downloads": self.cb_maxDownloads.isChecked(),
            "max_downloads": self.sb_maxDownloads.value(),
            "type": self.cb_type.currentIndex(),
            "quality_video": quality_video,
            "format_video": self.cb_fvideo.currentText(),
            "quality_audio": quality_audio,
            "format_audio": self.cb_faudio.currentText(),
            "cb_subtitles": self.cb_subtitles.isChecked(),
            "lang_subtitles": self.le_lang_subtitles.text(),
            "cb_cookies": self.cb_cookies.isChecked(),
            "cookies": self.le_cookies.text(),
            "cb_limit_rate": self.cb_limitRate.isChecked(),
            "limit_rate": limit_rate,
            "cb_proxy": self.cb_proxy.isChecked(),
            "proxy": proxy,
            "cb_thumbnail": self.cb_thumbnail.isChecked(),
            "cb_no_overwrites": self.cb_noOverwrites.isChecked(),
            "cb_metadata": self.cb_metadata.isChecked(),
            "cb_embed_subtitles": self.cb_embedSubs.isChecked(),
            "cb_restrict_filename": self.cb_restrictFilename.isChecked(),
            "cb_no_playlist": self.cb_noPlaylist.isChecked(),
            "cb_download_archive": self.cb_downloadArchive.isChecked(),
        }

        self.save_signal.emit(conf)
        self.close()

    def browse_path(self):
        file_path = QFileDialog.getExistingDirectory(
            self, "Select Download Folder")

        if file_path:
            self.le_path.setText(file_path)

    def revert_filename(self):
        self.le_filename.setText("%(title)s.%(ext)s")

    def browse_cookies(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", filter="Text Files (*.txt);;All Files (*)")

        if file_path:
            self.le_cookies.setText(file_path)


class ThumbnailLoader(QThread):
    finished = Signal(QPixmap, int)  # pixmap, row

    def __init__(self, url, row):
        super().__init__()
        self.url = url
        self.row = row

    def load_pixmap_from_url(self) -> QPixmap:
        try:
            response = get_request(self.url)
            if response.status_code == 200:
                img_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(img_data))
                return pixmap
        except Exception as e:
            print(f"Error loading image: {e}")
        return QPixmap()  # Empty image if failed

    def run(self):
        pixmap = self.load_pixmap_from_url()
        self.finished.emit(pixmap, self.row)


class DownloadTask:
    def __init__(self, url: str, options: dict = None):
        self.url = url
        self.output_template = "%(title)s.%(ext)s"
        self.options = []
        if options:
            self.build_options(options)
        self.process: subprocess.Popen | None = None
        self.state = "idle"  # idle, downloading, paused, completed
        self.metadata: dict = {}  # Dictionary with useful information
        self.retry_count = 0
        self.manual_pause = False

    def build_options(self, config: dict):
        # Output
        if config.get("path") and config.get("filename"):
            if config.get("path") == "default" and config.get("filename") == "default":
                self.output_template = (
                    Path(__file__).parent / "download" / "%(title)s.%(ext)s").__str__()

            elif config.get("path") == "default":
                self.output_template = (
                    Path(__file__).parent / "download" / config.get("filename")).__str__()

            elif config.get("filename") == "default":
                if config.get("path").endswith("/"):
                    self.output_template = config.get(
                        "path") + "%(title)s.%(ext)s"
                else:
                    self.output_template = config.get(
                        "path") + "/%(title)s.%(ext)s"

        else:
            self.output_template = (
                Path(__file__).parent / "download" / "%(title)s.%(ext)s").__str__()

        opts = []

        # Video/audio quality/format
        download_type = int(config.get("type", "0"))
        args = ["-f"]
        if download_type == 0:  # Video settings
            quality_map = {
                "Best": "bestvideo+bestaudio/best",
                "Worst": "worstvideo+worstaudio/worst",
            }
            advance = f"bv*[height<={config['quality_video'][:-1]}]+ba/b[height<={config['quality_video'][:-1]}]"
            mapped = quality_map.get(config['quality_video'], advance)

            args.extend([mapped, "--recode-video", config['format_video']])

        elif download_type == 1:  # Audio settings
            quality_map = {
                "Best": "bestaudio/best",
                "Worst": "worstaudio/worst",
            }
            advance = f"ba*[abr<={config['quality_audio'][:-1]}]/b[abr<={config['quality_audio'][:-1]}]"
            mapped = quality_map.get(config['quality_audio'], advance)

            args.extend([mapped, "--extract-audio",
                        "--audio-format", config['format_audio']])

        # Arguments have been separated from average
        # and general settings for better debugging.
        opts.extend(args)

        # Boundaries
        if config.get("cb_max_downloads"):
            opts += ["--max-downloads", config["max_downloads"]]
        if config.get("cb_limit_rate"):
            opts += ["--limit-rate", config["limit_rate"]]

        # Subtitles
        if config.get("cb_subtitles"):
            opts += ["--sub-lang", config["lang_subtitles"], "--write-subs"]
        if config.get("cb_embed_subtitles"):
            opts += ["--embed-subs"]

        # Cookies
        if config.get("cb_cookies"):
            opts += ["--cookies", config["cookies"]]

        # Proxy
        if config.get("cb_proxy"):
            opts += ["--proxy", config["proxy"]]

        # Restrictions and behavior
        if config.get("cb_thumbnail"):
            opts.append("--embed-thumbnail")
        if config.get("cb_no_overwrites"):
            opts.append("--no-overwrites")
        if config.get("cb_metadata"):
            opts.append("--add-metadata")
        if config.get("cb_restrict_filename"):
            opts.append("--restrict-filenames")
        if config.get("cb_no_playlist"):
            opts.append("--no-playlist")
        if config.get("cb_download_archive"):
            if config.get("path"):
                if config.get("path") == "default":
                    path = (Path(__file__).parent / "download" /
                            "downloaded.txt").__str__()
                else:
                    if config.get("path").endswith("/"):
                        path = config.get("path") + "downloaded.txt"
                    else:
                        path = config.get("path") + "/downloaded.txt"
                opts += ["--download-archive", path]

        self.options = opts

    def start(self):
        if self.process is not None and self.process.poll() is None:
            print(f"[{self.url}] already running")
            return  # It is already running

        cmd = [
            "yt-dlp",
            "-o", self.output_template,
            "--continue",  # Allows you to resume previous downloads
            *self.options,
            self.url
        ]

        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=creationflags
        )
        self.state = "downloading"
        print(f"[{self.url}] started (new process)")

    def cancel(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process = None
            self.state = "cancelled"
            print(f"[{self.url}] cancelled")

    def pause(self):
        self.manual_pause = True
        if self.process and self.process.poll() is None:
            if os.name == "nt":
                # Send CTRL_BREAK_EVENT on Windows
                self.process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # Send SIGINT (or SIGTERM if you prefer)
                self.process.send_signal(signal.SIGINT)

            self.process.wait()  # Wait for the process to close
            self.process = None
            self.state = "paused"
            print(f"[{self.url}] paused")

    def resume(self):
        if self.is_running():
            print(f"[{self.url}] already running, skipping resume")
            return
        if self.state != "paused":
            print(f"[{self.url}] not paused, can't resume")
            return
        self.manual_pause = False
        self.state = "downloading"
        self.start()
        print(f"[{self.url}] resumed")

    def is_running(self) -> bool:
        return self.process and self.process.poll() is None

    def is_completed(self) -> bool:
        return self.process and self.process.poll() == 0

    def validate_and_get_metadata(self) -> tuple[bool, str]:
        """
        Attempts to get metadata from the video. Returns:
        - (True, "valid") if it was obtained correctly and saved in self.metadata.
        - (False, "invalid_url" | "requires_login" | "error") if it failed.
        """
        # validate url
        parsed = urlparse(self.url)
        if not parsed.scheme in ("http", "https") and bool(parsed.netloc):
            return False, "invalid_url"

        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--quiet",
                "--no-warnings", "--dump-json", *self.options, self.url],
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            try:
                raw = json.loads(result.stdout)
                self.metadata = {
                    "id": raw.get("id", ""),
                    "title": raw.get("title", self.url),
                    "thumbnail": raw.get("thumbnail", ""),
                    "description": raw.get("description", ""),
                    "duration": self.format_duration(raw.get("duration", 0)),
                    "uploader": raw.get("uploader", "Unknown"),
                    "categories": raw.get("categories", []),
                    "tags": raw.get("tags", []),
                    "upload_date": self.format_date(raw.get("upload_date", "")),
                    "subtitles": raw.get("automatic_captions"),
                    "extractor_key": raw.get("extractor_key", ""),
                    "language": raw.get("language", ""),
                    "resolution": raw.get("resolution", ""),
                    "filesize": self.format_filesize(raw.get("filesize_approx", 0)),
                    "quality": raw.get("format", "").split(" - ")[1] if " - " in raw.get("format", "") else raw.get("format", ""),
                    "ext": raw.get("ext", "")
                }
                return True, "valid"
            except Exception as e:
                print("Error processing JSON:", e)
                return False, "error"

        err = result.stderr.lower()
        if "not a valid url" in err or "unsupported url" in err:
            return False, "invalid_url"
        elif "sign in" in err or "login" in err or "confirm you’re not a bot" in err:
            return False, "requires_login"
        else:
            return False, "error"

    @staticmethod
    def format_duration(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02}:{minutes:02}:{secs:02}"

    @staticmethod
    def format_filesize(bytes_size: int) -> str:
        mb = bytes_size / (1024 * 1024)
        if mb > 1000:
            gb = mb / 1024
            return f"{gb:.2f} GB"
        else:
            return f"{mb:.2f} MB"

    @staticmethod
    def format_date(date_str: str) -> str:
        try:
            if len(date_str) == 6:
                date_str = "20" + date_str
            if len(date_str) != 8:
                return date_str  # or you could return "Invalid Date"

            date_obj = datetime.strptime(date_str, "%Y%m%d")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return date_str  # or "Invalid Date"


class DownloadWorkerSignals(QObject):
    progress = Signal(int, str, str)  # percentage, speed, ETA
    finished = Signal(str)
    error = Signal(str)


class DownloadWorker(QRunnable):
    def __init__(self, mode: str, task: DownloadTask):
        """
        mode: "build" | "download | resume | paused"
        """
        super().__init__()
        self.mode = mode
        self.task = task
        self.signals = DownloadWorkerSignals()

    def __del__(self):
        print(f"[{self.task.url}] DownloadWorker removed")

    def convert_speed(self, speed_str: str) -> str:
        if not speed_str.endswith("MiB/s"):
            return speed_str  # It is already formatted or is not valid

        try:
            mib = float(speed_str.replace("MiB/s", "").strip())
            bps = mib * 1024 * 1024 * 8  # Convert MiB/s to bits per second
        except ValueError:
            return speed_str

        if bps >= 1_000_000_000:
            return f"{bps / 1_000_000_000:.2f} Gbps"
        elif bps >= 1_000_000:
            return f"{bps / 1_000_000:.2f} Mbps"
        elif bps >= 1_000:
            return f"{bps / 1_000:.2f} Kbps"
        else:
            return f"{bps:.0f} bps"

    def parse_progress(self, line: str) -> dict | None:
        import re
        match = re.search(
            r'\[download\]\s+([\d.]+)% of\s+([\d.]+\w+) at\s+([\d.]+\w+/s) ETA (\d+:\d+)', line)
        if match:
            data = {
                "progress": round(float(match.group(1))),
                # "total": match.group(2),
                "speed": self.convert_speed(match.group(3)),
                "eta": match.group(4)
            }
            return data
        return None

    def run(self):
        def retry_download(max_retries=3, delay=3):
            for attempt in range(1, max_retries + 1):
                if self.task.state in ("paused", "cancelled"):
                    print(
                        f"[{self.task.url}] Stopped manually, no retries")
                    return

                print(
                    f"[{self.task.url}] Retrying... ({attempt}/{max_retries})")
                self.task.start()
                self.task.process.wait()

                if self.task.is_completed():
                    self.signals.finished.emit(self.task.url)
                    return

                time.sleep(delay)

            self.signals.error.emit(
                f"Failure after {max_retries} attempts: {self.task.url}")

        try:
            if self.mode == "build":
                is_valid, status = self.task.validate_and_get_metadata()
                if not is_valid:
                    self.signals.error.emit(status)
                    return
                self.signals.finished.emit(self.task.url)

            elif self.mode in ("download", "resume"):
                self.task.start()
                for line in self.task.process.stdout:
                    line = line.strip()
                    if line.startswith("[download]"):
                        data = self.parse_progress(line)
                        if data:
                            self.signals.progress.emit(
                                data.get("progress"), data.get("speed"), data.get("eta"))

                self.task.process.wait()
                if self.task.is_completed():
                    self.task.state = "completed"
                    self.signals.finished.emit(self.task.url)
                else:
                    if self.task.state in ("paused", "cancelled"):
                        print(
                            f"[{self.task.url}] Stopped manually, no retries")
                        return
                    if not self.task.manual_pause:
                        retry_download()

            elif self.mode == "paused":
                self.task.pause()
                self.signals.finished.emit(self.task.url)

        except Exception as e:
            self.signals.error.emit(str(e))
