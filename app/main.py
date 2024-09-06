from os import path
from sys import argv

# from PySide6.QtCore import
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from gui.ui_app import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tw.setColumnWidth(0, 200)
        self.le_path.setText(path.expanduser("~\\Downloads"))
        self.statusBar.showMessage("Version 0.1 | by @Ec-25")
        self.show()

        self.index = 0
        self.to_download = {}
        self.threads = {}

        self.tb_filename.clicked.connect(self.reset_filename)
        self.tb_path.clicked.connect(self.select_path)
        self.ob_type.currentTextChanged.connect(self.update_type_media)

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


if __name__ == "__main__":
    # Start the application
    app = QApplication(argv)
    window = MainWindow()
    app.exit(app.exec())
