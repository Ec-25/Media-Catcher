import shutil
import platform
import stat
from os import environ, path, makedirs, pathsep, stat as stat_result, chmod
from sys import argv
from pathlib import Path

from PySide6 import QtCore as qtc, QtWidgets as qtw

from gui.ui_app import Ui_MainWindow
from gui.ui_download import Ui_Download
from threads import (
    DownloadThread,
    ItemWorker,
    V_FORMATS,
    V_FORMATS_SUPPORTING_THUMBNAILS,
    A_FORMATS_SUPPORTING_THUMBNAILS,
)


class DownloadWindow(qtw.QWidget, Ui_Download):
    finished = qtc.Signal()

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
            qtc.QTimer.singleShot(0, self.finished.emit)

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


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tw.setColumnWidth(0, 200)
        self.le_url.setFocus()
        self.le_path.setText(path.expanduser("~\\Downloads"))
        self.statusBar.showMessage("Version 0.1 | by @Ec-25")

        self.dwld = DownloadWindow()
        self.dwld.finished.connect(self.dwld.close)
        self.dwld.finished.connect(self.show)
        self.update_format_video()

        self.threadpool = qtc.QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        self.to_download = {}
        self.threads = {}
        self.index = 0

        self.tb_filename.clicked.connect(self.reset_filename)
        self.tb_path.clicked.connect(self.select_path)
        self.ob_type.currentTextChanged.connect(self.update_type_media)
        self.ob_fvideo.currentTextChanged.connect(self.update_format_video)
        self.ob_faudio.currentTextChanged.connect(self.update_format_audio)
        self.pb_add.clicked.connect(self.button_add)
        self.tw.itemClicked.connect(self.remove_item)
        self.pb_clear.clicked.connect(self.button_clear)
        self.pb_download.clicked.connect(self.button_download)

    def reset_filename(self):
        self.le_filename.setText("")

    def select_path(self):
        file_dialog = qtw.QFileDialog()
        file_dialog.setFileMode(qtw.QFileDialog.FileMode.Directory)
        file_dialog.setOption(qtw.QFileDialog.Option.ShowDirsOnly)
        file_dialog.exec()
        self.le_path.setText(
            file_dialog.selectedFiles()[0]
            if len(file_dialog.selectedFiles()) > 0
            else ""
        )

    def update_type_media(self):
        if self.ob_type.currentText() == "Video":
            self.update_format_video()
            self.ob_qvideo.setEnabled(True)
            self.ob_fvideo.setEnabled(True)
            self.cb_subtitles.setEnabled(True)

        elif self.ob_type.currentText() == "Audio":
            self.ob_qvideo.setEnabled(False)
            self.ob_fvideo.setEnabled(False)
            self.ob_faudio.setEnabled(True)
            self.cb_subtitles.setChecked(False)
            self.cb_subtitles.setEnabled(False)

            if self.ob_faudio.currentText().lower() in A_FORMATS_SUPPORTING_THUMBNAILS:
                self.cb_thumbnail.setEnabled(True)
            else:
                self.cb_thumbnail.setChecked(False)
                self.cb_thumbnail.setEnabled(False)

    def update_format_video(self):
        current_fvideo = self.ob_fvideo.currentText().lower()
        self.ob_faudio.setCurrentText(V_FORMATS[current_fvideo]["audio"])
        self.ob_faudio.setEnabled(False)

        if current_fvideo in V_FORMATS_SUPPORTING_THUMBNAILS:
            self.cb_thumbnail.setEnabled(True)
        else:
            self.cb_thumbnail.setChecked(False)
            self.cb_thumbnail.setEnabled(False)

    def update_format_audio(self):
        if self.ob_type.currentText() == "Audio":
            if self.ob_faudio.currentText().lower() in A_FORMATS_SUPPORTING_THUMBNAILS:
                self.cb_thumbnail.setEnabled(True)
            else:
                self.cb_thumbnail.setChecked(False)
                self.cb_thumbnail.setEnabled(False)

    def remove_item(self, item, column):
        ret = qtw.QMessageBox.question(
            self,
            "Application Message",
            f"Would you like to remove {item.text(0)} ?",
            qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No,
            qtw.QMessageBox.StandardButton.No,
        )
        if ret == qtw.QMessageBox.StandardButton.Yes:
            if self.to_download.get(item.id):
                self.to_download.pop(item.id)
            elif threads := self.threads.get(item.id):
                threads.stop()
            self.tw.takeTopLevelItem(self.tw.indexOfTopLevelItem(item))

    def button_add(self):
        url = self.le_url.text()
        path = self.le_path.text()
        filename = self.le_filename.text()
        if not filename:
            filename = "%(title)s.%(ext)s"
        type = self.ob_type.currentText()
        subtitles = self.cb_subtitles.isChecked()
        sublangs = self.le_subtitles.text()
        qvideo = self.ob_qvideo.currentText()
        fvideo = self.ob_fvideo.currentText()
        qaudio = self.ob_qaudio.currentText()
        faudio = self.ob_faudio.currentText()
        metadata = self.cb_metadata.isChecked()
        thumbnail = self.cb_thumbnail.isChecked()
        noplaylist = self.cb_noplaylist.isChecked()

        if not all([url, path, type]):
            return qtw.QMessageBox.information(
                self,
                "Application Message",
                "Unable to add the download because some required fields are missing.\nRequired fields: Link, Path & Format.",
            )

        item = qtw.QTreeWidgetItem(self.tw, [url, type, "-", "0%", "Queued", "-", "-"])
        pb = qtw.QProgressBar()
        pb.setStyleSheet("QProgressBar { margin-bottom: 3px; }")
        pb.setTextVisible(False)
        self.tw.setItemWidget(item, 3, pb)
        item.id = self.index  # type: ignore
        self.le_url.clear()
        self.to_download[self.index] = ItemWorker(
            item,
            url,
            path,
            filename,
            type,
            subtitles,
            sublangs,
            qvideo,
            fvideo,
            qaudio,
            faudio,
            metadata,
            thumbnail,
            noplaylist,
        )
        self.index += 1

    def button_clear(self):
        if self.threads:
            return qtw.QMessageBox.critical(
                self,
                "Application Message",
                "Unable to clear list because there are active downloads in progress.\n"
                "Remove a download by clicking on it.",
            )

        self.threads = {}
        self.to_download = {}
        self.index = 0
        self.tw.clear()

    def button_download(self):
        if not self.to_download:
            return qtw.QMessageBox.information(
                self,
                "Application Message",
                "Unable to download because there are no links in the list.",
            )

        for index, worker in self.to_download.items():
            self.threads[index] = worker
            self.threads[index].signals.finished.connect(lambda x: self.threads.pop(x))
            self.threads[index].signals.progress.connect(self.update_progress)

            self.threadpool.start(self.threads[index])

        self.to_download = {}

    def update_progress(self, item, emit_data):
        try:
            for data in emit_data:
                index, update = data
                if index != 3:
                    item.setText(index, update)
                else:
                    pb = self.tw.itemWidget(item, index)
                    pb.setValue(round(float(update.replace("%", ""))))  # type: ignore
        except AttributeError:
            return qtw.QMessageBox.information(
                self,
                "Application Error",
                f"Download ({item.id}) no longer exists",
            )


if __name__ == "__main__":
    ROOT = Path(__file__).parent
    environ["PATH"] += pathsep + str(ROOT / "bin")
    # Start the application
    app = qtw.QApplication(argv)
    window = MainWindow()
    app.exit(app.exec())
