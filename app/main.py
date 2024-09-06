import shutil
import platform
import stat
from os import environ, path, makedirs, pathsep, stat as stat_result, chmod
from sys import argv
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QMessageBox, QTreeWidgetItem, QProgressBar

from gui.ui_app import Ui_MainWindow
from gui.ui_download import Ui_Download
from threads import DownloadThread


class DownloadWindow(QWidget, Ui_Download):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb.setMaximum(100)
        self.missing = []

        self.get_missings()

        if self.missing:
            self.show()
            self.start_download()
        else:
            QTimer.singleShot(0, self.finished.emit)

    def get_missings(self):
        binaries = {
            "Darwin": {
                "ffmpeg": "ffmpeg-osx64-v4.1",
                "ffprobe": "ffprobe-osx64-v4.1",
                "yt-dlp": "yt-dlp_macos",
            },
            "Linux": {
                "ffmpeg": "ffmpeg-linux64-v4.1",
                "ffprobe": "ffprobe-linux64-v4.1",
                "yt-dlp": "yt-dlp_linux",
            },
            "Windows": {
                "ffmpeg": "ffmpeg-win64-v4.1.exe",
                "ffprobe": "ffprobe-win64-v4.1.exe",
                "yt-dlp": "yt-dlp.exe",
            },
        }

        missing_path_env = [
            exe for exe in ["ffmpeg", "ffprobe", "yt-dlp"] if not shutil.which(exe)
        ]
        os_ = platform.system()

        if missing_path_env:
            BINARIES = ROOT / "bin"
            if not path.exists(BINARIES):
                makedirs(BINARIES)

            for exe in missing_path_env:
                if exe == "yt-dlp":
                    url = f"https://github.com/yt-dlp/yt-dlp/releases/latest/download/{binaries[os_][exe]}"

                elif exe == "ffmpeg" or exe == "ffprobe":
                    url = f"https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{binaries[os_][exe]}"

                filename = path.join(
                    BINARIES, f"{exe}.exe" if os_ == "Windows" else f"{exe}"
                )
                self.missing.append((url, filename))

    def start_download(self):
        url, filename = self.missing[0]
        self.downloader = DownloadThread(url, filename)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.downloader.finished.connect(self.download_finished)
        self.downloader.start()

    def update_progress(self, progress, text):
        self.pb.setValue(progress)
        self.lb_progress.setText(text)

    def download_finished(self):
        url, filename = self.missing.pop(0)
        st = stat_result(filename)
        chmod(filename, st.st_mode | stat.S_IEXEC)

        if self.missing:
            self.start_download()
        else:
            self.finished.emit()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tw.setColumnWidth(0, 200)
        self.le_path.setText(path.expanduser("~\\Downloads"))
        self.statusBar.showMessage("Version 0.1 | by @Ec-25")

        self.dwld = DownloadWindow()
        self.dwld.finished.connect(self.dwld.close)
        self.dwld.finished.connect(self.show)

        self.index = 0
        self.to_download = {}
        self.threads = {}

        self.tb_filename.clicked.connect(self.reset_filename)
        self.tb_path.clicked.connect(self.select_path)
        self.ob_type.currentTextChanged.connect(self.update_type_media)
        self.pb_add.clicked.connect(self.add_url)
        self.tw.itemClicked.connect(self.remove_item)
        self.pb_clear.clicked.connect(self.clear_list)

    def reset_filename(self):
        self.le_filename.setText("")

    def select_path(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly)
        file_dialog.exec()
        self.le_path.setText(
            file_dialog.selectedFiles()[0]
            if len(file_dialog.selectedFiles()) > 0
            else ""
        )

    def update_type_media(self):
        if self.ob_type.currentText() == "Video":
            self.ob_qvideo.setEnabled(True)
            self.ob_fvideo.setEnabled(True)
            self.cb_subtitles.setEnabled(True)

        elif self.ob_type.currentText() == "Audio":
            self.ob_qvideo.setEnabled(False)
            self.ob_fvideo.setEnabled(False)
            self.cb_subtitles.setChecked(False)
            self.cb_subtitles.setEnabled(False)

    def add_url(self):
        url = self.le_url.text()
        path = self.le_path.text()
        fmt = self.ob_type.currentText()

        if not all([url, path, fmt]):
            return QMessageBox.information(self, "Application Message", "Unable to add the download because some required fields are missing.\nRequired fields: Link, Path & Format.")

        item = QTreeWidgetItem(self.tw, [url, fmt, "-", "0%", "Queued", "-", "-"])
        pb = QProgressBar()
        pb.setStyleSheet("QProgressBar { margin-bottom: 3px;}")
        pb.setTextVisible(False)
        self.tw.setItemWidget(item, 3, pb)

        item.id = self.index # type: ignore
        self.le_url.clear()

        self.index += 1

    def remove_item(self):
        confirm = QMessageBox.question(self, "Application Message", "Are you sure you want to remove this item?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            if self.to_download.get(self.tw.currentItem().id): # type: ignore
                self.to_download.pop(self.tw.currentItem().id) # type: ignore


            self.tw.takeTopLevelItem(self.tw.indexOfTopLevelItem(self.tw.currentItem()))

    def clear_list(self):
        if self.threads:
            return QMessageBox.information(self, "Application Message", "Unable to clear the list because there is a download in progress.")
        
        self.threads = {}
        self.to_download = {}
        self.tw.clear()

if __name__ == "__main__":
    ROOT = Path(__file__).parent
    environ["PATH"] += pathsep + str(ROOT / "bin")
    # Start the application
    app = QApplication(argv)
    window = MainWindow()
    app.exit(app.exec())
