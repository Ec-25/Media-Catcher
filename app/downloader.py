from datetime import datetime
import subprocess
import json


class DownloadTask:
    def __init__(self, url: str, output_template: str = "%(title)s.%(ext)s", options: list[str] = None):
        self.url = url
        self.output_template = output_template
        self.options = options or []
        self.process: subprocess.Popen | None = None
        self.state = "idle"  # idle, downloading, paused, cancelled, completed
        self.metadata: dict = {}  # Dictionary with useful information

    def start(self):
        if self.process is not None:
            return  # It is already running

        cmd = [
            "yt-dlp",
            "-o", self.output_template,
            "--continue",  # Allows you to resume previous downloads
            *self.options,
            self.url
        ]

        self.process = subprocess.Popen(cmd)
        self.state = "downloading"
        print(f"[{self.url}] started")

    def cancel(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process = None
            self.state = "cancelled"
            print(f"[{self.url}] cancelled")

    def pause(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()  # simulate pause
            self.process = None
            self.state = "paused"
            print(f"[{self.url}] paused")

    def resume(self):
        if self.state == "paused":
            self.start()
            print(f"[{self.url}] resumed")

    def is_running(self) -> bool:
        return self.process and self.process.poll() is None

    def is_completed(self) -> bool:
        return self.process and self.process.poll() == 0

    def is_url_valid(self) -> tuple[bool, str]:
        """
        Verifica si la URL es válida (soportada por yt-dlp).
        Devuelve True|False si es valido y el detalle:
            - 'valid'
            - 'invalid_format'
            - 'requires_login'
            - 'error'
        """
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--quiet",
                "--no-warnings", "--dump-json", self.url],
            capture_output=True,
            text=True
        )
        # If stdout has info, it is valid
        if result.stdout.strip():
            return True, "valid"

        err = result.stderr.lower()
        if "not a valid url" in err or "unsupported url" in err:
            return False, "invalid_url"
        elif "sign in" in err or "login" in err or "confirm you’re not a bot" in err:
            return False, "requires_login"
        else:
            return False, "error"

    def get_info(self) -> bool:
        """Extrae y guarda metadata útil del video. Devuelve True si fue exitoso."""
        try:
            result = subprocess.run(
                ["yt-dlp", "--skip-download", "--dump-json", self.url],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                raw = json.loads(result.stdout)

                # set metadata
                self.metadata = {
                    "id": raw.get("id", ""),
                    "title": raw.get("title", self.url),
                    "thumbnail": raw.get("thumbnail", ""),
                    "description": raw.get("description", ""),
                    "duration": DownloadTask.format_duration(raw.get("duration", 0)),
                    "uploader": raw.get("uploader", "Desconocido"),
                    "categories": raw.get("categories", []),
                    "tags": raw.get("tags", []),
                    "upload_date": DownloadTask.format_date(raw.get("upload_date", "")),
                    "subtitles": raw.get("automatic_captions"),
                    "extractor_key": raw.get("extractor_key", ""),
                    "language": raw.get("language", ""),
                    "resolution": raw.get("resolution", ""),
                    "filesize": DownloadTask.format_filesize(raw.get("filesize_approx", 0)),
                    "quality": raw.get("format", "").split(" - ")[1],
                    "ext": raw.get("ext", "")
                }

                return True

            else:
                print("Error al extraer metadata:", result.stderr.strip())
                return False

        except Exception as e:
            print("Excepción en get_info:", str(e))
            return False

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
