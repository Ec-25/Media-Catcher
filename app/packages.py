from os import path, environ, pathsep, makedirs
from shutil import which
from platform import system
from pathlib import Path
import stat
import subprocess
import requests

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
        List of (url, expected_path) tuples for missing executables, or None if all are found.
    """
    packages = ['yt-dlp', 'ffmpeg', 'ffprobe']
    os_ = system()
    bin_path = ROOT / "bin"
    missing = []

    for exe in packages:
        found = which(exe)

        # If it is not in the system PATH
        if not found:
            # Try searching in ROOT/bin
            expected_name = exe if os_ != "Windows" else f"{exe}.exe"
            local_path = bin_path / expected_name

            if local_path.exists():
                # If present, add to PATH
                add_to_path(bin_path)
            else:
                # If not anywhere, mark for download
                url = DOWNLOAD_PACKAGES_INFO[exe]
                file_request = bin_path / _REQUIRED_PACKAGES_INFO[os_][exe]
                missing.append((url, file_request))

    return missing if missing else None


def add_to_path(bin_path: Path) -> None:
    """Add the bin folder to the user PATH without duplicating or injecting system PATH (Windows-safe)."""
    bin_str = str(bin_path)

    current_path = environ.get("PATH", "")
    if bin_str in current_path.split(pathsep):
        return  # It's already on the PATH

    if _OS == "Windows":
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
                user_path, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            user_path = ""

        # Separate and clean entrances
        paths = [p.strip() for p in user_path.split(";") if p.strip()]
        if bin_str not in paths:
            paths.append(bin_str)
            new_path = ";".join(paths)

            subprocess.run(
                ['setx', 'PATH', new_path],
                shell=True,
                check=False,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            )

    else:
        # For Linux/macOS, we add it to ~/.bashrc or ~/.zshrc if it is not there
        shell_config = path.expanduser("~/.bashrc")
        if environ.get("SHELL", "").endswith("zsh"):
            shell_config = path.expanduser("~/.zshrc")

        if path.exists(shell_config):
            with open(shell_config, "r+") as f:
                content = f.read()
                if bin_str not in content:
                    f.write(f'\nexport PATH="{bin_str}:$PATH"\n')


def download_missing(missing: list[tuple[str, str]], loading_dialog: LoadingDialog, ROOT: Path) -> bool:
    """
    Download missing executables from the provided URLs, rename them properly,
    and make them executable on Linux/macOS.
    """
    failed = False
    bin_path = ROOT / "bin"
    makedirs(bin_path, exist_ok=True)

    total_files = len(missing)
    index = 0

    for index, (url, _) in enumerate(missing, start=1):
        filename = path.basename(url)

        # Normalize name according to rules
        if filename.startswith("yt-dlp"):
            base_name = "yt-dlp"
        elif filename.startswith("ffmpeg") or filename.startswith("ffprobe"):
            base_name = filename.split("-")[0]
        else:
            base_name = filename  # If no rule matches

        # Add extension
        if _OS == "Windows":
            file_name = base_name + ".exe"
            file_path = bin_path / file_name
        else:
            file_path = bin_path / base_name

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get(
                    "content-length", 0))  # Total size in bytes
                downloaded_size = 0

                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)

                            # Calculate progress
                            percent = int((downloaded_size / total_size)
                                          * 100) if total_size else 100
                            loading_dialog.set_value_loading(percent)
                            QCoreApplication.processEvents()  # Force UI refresh

                # Adding execute permissions on UNIX systems
                if _OS != "Windows":
                    file_path.chmod(file_path.stat().st_mode | stat.S_IXUSR)

            else:
                print(f"Error al descargar {url}")
                failed = True
        except Exception as e:
            print(f"Excepción al descargar {url}: {e}")
            failed = True

        # Update progress bar based on downloaded files
        loading_dialog.set_value_loading(int((index / total_files) * 100))

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
