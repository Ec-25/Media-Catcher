from os import makedirs, path, name as os_name
from shutil import which
from platform import system
import subprocess
from requests import get as get_request
from pathlib import Path

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QCoreApplication

from gui.dialog import Ui_Dialog


class LoadingDialog(QDialog, Ui_Dialog):
    def __init__(self, lang: str):
        super().__init__()
        self.lang = lang
        self.dictionary = {
            "es": {
                "title": "Cargando...",
                "text": "Cargando Contenido...",
                "dependencies": "Comprobando dependencias...",
                "download": "Descargando paquetes..."
            },
            "en": {
                "title": "Loading...",
                "text": "Loading Content...",
                "dependencies": "Checking dependencies...",
                "download": "Downloading packages..."
            }
        }
        self.setupUi(self)
        self.setWindowTitle(self.dictionary[self.lang]["title"])
        self.label.setText(self.dictionary[self.lang]["text"])
        self.show()

    def set_text_loading(self, text):
        self.label.setText(self.dictionary[self.lang][text])

    def set_value_loading(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            self.close()


def check_dependencies() -> list:
    """
    Check for the presence of required dependencies and provide suggestions for installation.

    If any of the dependencies are not found, it prints a message with suggestions
    for installation.
    """
    dependencies = ['PySide6', 'requests']
    not_found = []

    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            not_found.append(dep)

    return not_found


def check_packages(ROOT: Path) -> list[tuple[str, str]] | None:
    """
    Check if the packages are available on the system or in the bin folder.

    Returns:
    None
    """
    packages = ['yt-dlp', 'ffmpeg', 'ffprobe']
    os_ = system()

    missing_exes = [
        exe for exe in packages if not which(exe)
    ]

    if missing_exes:
        missing = []

        bin_path = ROOT / "bin"

        for exe in missing_exes:
            url = DOWNLOAD_PACKAGES_INFO[exe]
            filename = path.join(bin_path, _REQUIRED_PACKAGES_INFO[os_][exe])

            missing.append((url, filename))

        return missing

    return None


def add_to_path(bin_path: Path) -> None:
    """Add the bin folder to the system PATH."""
    bin_str = str(bin_path)

    if system() == "Windows":
        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            if os_name == "nt" else 0
        )
        # Add to PATH in Windows (persistently)
        subprocess.run(
            f'setx PATH "%PATH%;{bin_str}"',
            shell=True,
            check=False,
            creationflags=creationflags
        )
    else:
        # Add to PATH on Linux/macOS (for the current session)
        shell_config = path.expanduser(
            "~/.bashrc")  # Or ~/.zshrc depending on the shell
        with open(shell_config, "a") as f:
            f.write(f'\nexport PATH="{bin_str}:$PATH"\n')


def download_missing(missing: list[tuple[str, str]], loading_dialog: LoadingDialog, ROOT: Path) -> bool:
    """
    Download missing executables from the provided URLs.

    Args:
    missing (list[tuple[str, str]]): A list of tuples containing the download URL and filename.
    loading_dialog (LoadingDialog): Reference to the upload dialog.
    """
    failed = False
    bin_path = ROOT / "bin"
    makedirs(bin_path, exist_ok=True)

    total_files = len(missing)
    for index, (url, filename) in enumerate(missing, start=1):
        file_path = path.join(bin_path, path.basename(url))
        response = get_request(url, stream=True)

        if response.status_code == 200:
            total_size = int(response.headers.get(
                "content-length", 0))  # Total size in bytes
            downloaded_size = 0

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)

                        # Calculate progress
                        percent = int((downloaded_size / total_size)
                                      * 100) if total_size else 100
                        loading_dialog.set_value_loading(percent)
                        QCoreApplication.processEvents()  # Force UI refresh

        else:
            failed = True
            return failed

        # Update progress bar based on downloaded files
        loading_dialog.set_value_loading(int((index / total_files) * 100))

        # Add the bin folder to the system PATH
        add_to_path(bin_path)
        return failed


def write_debug_log(message):
    """Write a log message to a file."""
    log_file = "debug.log"
    with open(log_file, "a") as f:
        f.write(str(message) + "\n")


_OS = system()
_REQUIRED_PACKAGES_INFO = {
    "Darwin": {
        "ffmpeg": "ffmpeg-osx64-v4.2.2",
        "ffprobe": "ffprobe-osx64-v4.1",
        "yt-dlp": "yt-dlp_macos",
    },
    "Linux": {
        "ffmpeg": "ffmpeg-linux64-v4.2.2",
        "ffprobe": "ffprobe-linux64-v4.1",
        "yt-dlp": "yt-dlp_linux",
    },
    "Windows": {
        "ffmpeg": "ffmpeg-win64-v4.2.2.exe",
        "ffprobe": "ffprobe-win64-v4.1.exe",
        "yt-dlp": "yt-dlp.exe",
    },
}
DOWNLOAD_PACKAGES_INFO = {
    'yt-dlp': f'https://github.com/yt-dlp/yt-dlp/releases/latest/download/{_REQUIRED_PACKAGES_INFO[_OS]['yt-dlp']}',
    'ffmpeg': f'https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{_REQUIRED_PACKAGES_INFO[_OS]['ffmpeg']}',
    'ffprobe': f'https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{_REQUIRED_PACKAGES_INFO[_OS]['ffprobe']}'
}
