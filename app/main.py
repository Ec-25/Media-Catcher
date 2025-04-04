from os import makedirs, path
from shutil import which
from platform import system
import subprocess
from requests import get as get_request
from pathlib import Path
from sys import exit as sys_exit, argv as sys_argv
from configparser import ConfigParser

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PySide6.QtCore import QCoreApplication

from gui.dialog import Ui_Dialog
from gui.main import Ui_MainWindow
from gui.config import Ui_Dialog as Ui_ConfigDialog

from packages import DOWNLOAD_PACKAGES_INFO, _REQUIRED_PACKAGES_INFO
from translations import translations


class LoadingDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.lang = get_config_value("general", "lang", "en")
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


class MainWindow(QMainWindow, Ui_MainWindow):
    # Configuration
    def __init__(self):
        super().__init__()
        self.lang = get_config_value("general", "lang", "en")
        self.dictionary = translations[self.lang]
        self.setupUi(self)
        self.init_language()
        self.awaitLoad()
        self.connectEvents()

    def awaitLoad(self):
        """Load all essential content"""
        # Show the loading window
        self.loading_dialog = LoadingDialog()

        self.loading_dialog.set_text_loading("dependencies")
        dependencies_not_found = check_dependencies()
        self.loading_dialog.set_value_loading(10)

        if len(dependencies_not_found) != 0:
            # display error message
            error = QMessageBox(self)
            error.setIcon(QMessageBox.Critical)
            error.setWindowTitle("Error")
            error.setText(
                self.dictionary["errors"]["dependencies_not_found"] + "\n".join(dependencies_not_found))
            error.setStandardButtons(QMessageBox.Ok)
            error.exec()
            sys_exit(1)

        missing = check_packages()
        self.loading_dialog.set_value_loading(20)

        if missing:
            self.loading_dialog.set_text_loading("download")
            failed = download_missing(missing, self.loading_dialog)

            if failed:
                error = QMessageBox(self)
                error.setIcon(QMessageBox.Critical)
                error.setWindowTitle("Error")
                error.setText(
                    self.dictionary["errors"]["download_dep"])
                error.setStandardButtons(QMessageBox.Ok)
                error.exec()
                sys_exit(1)

        # Loading finished, show main window
        self.loading_dialog.set_value_loading(100)
        self.loading_dialog.close()
        self.show()

    def init_language(self):
        """Initialize the language of the application"""
        # set the language that should be active
        if self.lang == "es":
            self.actionEnglish.setChecked(False)
            self.actionSpanish.setChecked(True)
        else:
            self.actionEnglish.setChecked(True)
            self.actionSpanish.setChecked(False)

        # set the language in the UI
        self.setWindowTitle(self.dictionary["title"])

        self.menuEdit.setTitle(self.dictionary["menu"]["edit"])
        self.menuFile.setTitle(self.dictionary["menu"]["file"])
        self.menuHelp.setTitle(self.dictionary["menu"]["help"])
        self.menuLanguage.setTitle(self.dictionary["menu"]["language"])

        self.actionExit.setText(self.dictionary["menuActions"]["exit"])
        self.actionSave_History.setText(
            self.dictionary["menuActions"]["saveHistory"])
        self.actionConfiguration.setText(
            self.dictionary["menuActions"]["configuration"])
        self.actionClear_List.setText(
            self.dictionary["menuActions"]["clearList"])
        self.actionAbout.setText(self.dictionary["menuActions"]["about"])

        self.inputUrl.setPlaceholderText(
            self.dictionary["elements"]["placeHolders"]["inputUrl"])
        self.btnAddUrl.setText(self.dictionary["elements"]["buttons"]["add"])
        self.tableMediaContent.horizontalHeader().setVisible(True)

    def set_language(self, lang):
        # set the language in the application and in the settings
        self.lang = lang
        set_config_value("general", "lang", lang)
        self.dictionary = translations[lang]

        self.init_language()

    def connectEvents(self):
        """Connect all senders to their respective events"""
        self.actionEnglish.triggered.connect(lambda: self.set_language("en"))
        self.actionSpanish.triggered.connect(lambda: self.set_language("es"))
        self.actionExit.triggered.connect(QApplication.instance().quit)
        self.actionAbout.triggered.connect(self.event_actionAbout)
        self.actionConfiguration.triggered.connect(
            self.event_actionConfiguration)

    def event_actionAbout(self):
        """Event for the About action"""
        QMessageBox.information(
            self,
            self.dictionary["about"]["title"],
            self.dictionary["about"]["text"]
        )

    def event_actionConfiguration(self):
        """Event for the Configuration action"""
        if not hasattr(self, 'config_window'):
            self.config_window = ConfigWindow()

        elif not self.config_window.isVisible():
            self.config_window.reload_language()
            self.config_window.show()
        else:
            self.config_window.reload_language()
            self.config_window.raise_()
            self.config_window.activateWindow()


class ConfigWindow(QDialog, Ui_ConfigDialog):
    def __init__(self):
        super().__init__()
        self.lang = get_config_value("general", "lang", "en")
        self.dictionary = translations[self.lang]
        self.setupUi(self)
        self.init_language()
        self.show()

    def set_language(self, lang):
        # set the language in the application and in the settings
        self.lang = lang
        set_config_value("general", "lang", lang)
        self.dictionary = translations[lang]

        self.init_language()

    def reload_language(self):
        """Reload the language of the application"""
        self.set_language(get_config_value("general", "lang"))

    def init_language(self):
        self.setWindowTitle(self.dictionary["configuration"]["title"])
        self.buttonBox.buttons()[0].setText(
            self.dictionary["configuration"]["save"])
        self.buttonBox.buttons()[1].setText(
            self.dictionary["configuration"]["cancel"])


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


def check_packages() -> list[tuple[str, str]] | None:
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
        # Add to PATH in Windows (persistently)
        subprocess.run(
            f'setx PATH "%PATH%;{bin_str}"',
            shell=True,
            check=False,
        )
    else:
        # Add to PATH on Linux/macOS (for the current session)
        shell_config = path.expanduser(
            "~/.bashrc")  # Or ~/.zshrc depending on the shell
        with open(shell_config, "a") as f:
            f.write(f'\nexport PATH="{bin_str}:$PATH"\n')


def download_missing(missing: list[tuple[str, str]], loading_dialog: LoadingDialog) -> bool:
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


def get_config_value(section: str, key: str, default: str = None) -> str:
    """Gets a value from the configuration dictionary."""
    value = CONFIG.get(section, {}).get(key)
    if value:
        return value

    elif not value and default:
        set_config_value(section, key, default)
        return default

    else:
        raise KeyError(f"Key '{key}' not found in the .cfg file.")


def set_config_value(section: str, key: str, value: str) -> None:
    """Updates a value in the dictionary and in the .cfg file."""
    # Update in the parser
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, value)

    from io import StringIO
    buffer = StringIO()
    parser.write(buffer)

    # Clean up extra blank lines
    lines = buffer.getvalue().splitlines()
    while lines and lines[-1].strip() == "":
        lines.pop()
    lines.append("")  # Just one trailing blank line

    with open(ROOT / "main.cfg", "w", encoding="utf-8") as config_file:
        config_file.write("\n".join(lines))

    # Update in-memory dictionary
    CONFIG.setdefault(section, {})[key] = value


if __name__ == "__main__":
    # config
    ROOT = Path(__file__).parent
    parser = ConfigParser()
    parser.read(ROOT / "main.cfg")
    CONFIG = {section: dict(parser.items(section))
              for section in parser.sections()}
    # ui
    app = QApplication(sys_argv)
    window = MainWindow()
    sys_exit(app.exec())
