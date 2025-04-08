from datetime import datetime
from pathlib import Path
from sys import exit as sys_exit, argv as sys_argv
from configparser import ConfigParser

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QProgressBar, QPushButton
from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PySide6.QtCore import QThreadPool

from packages import LoadingDialog, check_dependencies, check_packages, download_missing
from downloader import ConfigWindow, ThumbnailLoader, DownloadTask, DownloadWorker

from gui.main import Ui_MainWindow
from gui.history import Ui_History

from translations import translations


class HistoryDialog(QDialog, Ui_History):
    actionSignal = Signal(str)

    def __init__(self, lang: str, history: str):
        super().__init__()
        self.lang = lang
        self.dictionary = translations[self.lang]
        self.history = history
        self.setupUi(self)
        self.init_language()
        self.connectEvents()
        self.show()

    def init_language(self):
        self.setWindowTitle(self.dictionary["history"]["title"])
        self.label.setText(self.dictionary["history"]["label"])
        self.textEdit.setPlaceholderText(
            self.dictionary["history"]["placeholder"])
        self.textEdit.setText(self.history)
        self.btnSaveHistory.setText(self.dictionary["history"]["save"])
        self.btnDeleteHistory.setText(self.dictionary["history"]["delete"])

    def reload_language(self, lang: str):
        """Reload the language of the application"""
        # set the language in the application and in the settings
        self.lang = lang
        self.dictionary = translations[lang]

        self.init_language()

    def emitSignal(self, action: str):
        self.actionSignal.emit(action)

    def connectEvents(self):
        window.close_all.connect(self.close)
        self.btnSaveHistory.clicked.connect(self.save_history)
        self.btnDeleteHistory.clicked.connect(self.delete_history)

    def save_history(self):
        self.emitSignal("save")

    def delete_history(self):
        self.emitSignal("delete")


class MainWindow(QMainWindow, Ui_MainWindow):
    close_all = Signal()
    # Configuration

    def __init__(self):
        super().__init__()
        self.lang = get_config_value("general", "lang", "en")
        self.dictionary = translations[self.lang]
        self.setupUi(self)
        self.awaitLoad()
        self.init_language()
        self.connectEvents()
        self.thread_pool = QThreadPool.globalInstance()
        self.workers = {}
        self.thumbnail_threads = []
        self.show()

    def closeEvent(self, event):
        self.close_all.emit()
        event.accept()

    def awaitLoad(self):
        """Load all essential content"""
        # Show the loading window
        self.loading_dialog = LoadingDialog(self.lang)

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

        missing = check_packages(ROOT)
        self.loading_dialog.set_value_loading(20)

        if missing:
            self.loading_dialog.set_text_loading("download")
            failed = download_missing(missing, self.loading_dialog, ROOT)

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

        # prepare the table view
        self.prepare_table()

        # resize the main window
        w = 1287
        h = 640
        self.resize(w, h)

    def prepare_table(self):
        self.table_model = QStandardItemModel()
        self.table_model.setColumnCount(7)

        self.tableMediaContent.setModel(self.table_model)
        self.tableMediaContent.setColumnWidth(0, 400)  # title
        self.tableMediaContent.setColumnWidth(1, 100)  # duration
        self.tableMediaContent.setColumnWidth(2, 100)  # file size
        self.tableMediaContent.setColumnWidth(3, 400)  # progress bar
        self.tableMediaContent.setColumnWidth(4, 100)  # speed
        self.tableMediaContent.setColumnWidth(5, 100)  # time remaining
        self.tableMediaContent.setColumnWidth(6, 50)  # btn action
        self.tableMediaContent.setIconSize(QSize(53, 42))
        self.tableMediaContent.horizontalHeader().setVisible(True)

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

        # menu bar
        self.menuEdit.setTitle(self.dictionary["menu"]["edit"])
        self.menuFile.setTitle(self.dictionary["menu"]["file"])
        self.menuHelp.setTitle(self.dictionary["menu"]["help"])
        self.menuLanguage.setTitle(self.dictionary["menu"]["language"])

        # menu actions
        self.actionExit.setText(self.dictionary["menuActions"]["exit"])
        self.actionHistory.setText(
            self.dictionary["menuActions"]["history"])
        self.actionConfiguration.setText(
            self.dictionary["menuActions"]["configuration"])
        self.actionClear_List.setText(
            self.dictionary["menuActions"]["clearList"])
        self.actionAbout.setText(self.dictionary["menuActions"]["about"])

        # ui elements
        self.inputUrl.setPlaceholderText(
            self.dictionary["elements"]["placeHolders"]["inputUrl"])
        self.btnAddUrl.setText(self.dictionary["elements"]["buttons"]["add"])

        self.set_table_headers()

    def set_table_headers(self):
        self.table_model.setHorizontalHeaderLabels(
            [self.dictionary["elements"]["table_model"]["title"], self.dictionary["elements"]["table_model"]["duration"], self.dictionary["elements"]["table_model"]["size"], self.dictionary["elements"]["table_model"]["downloaded"], self.dictionary["elements"]["table_model"]["speed"], self.dictionary["elements"]["table_model"]["time_remaining"], self.dictionary["elements"]["table_model"]["action"]])

    def set_language(self, lang):
        # set the language in the application and in the settings
        self.lang = lang
        set_config_value("general", "lang", lang)
        self.dictionary = translations[lang]

        self.init_language()

    def connectEvents(self):
        """Connect all senders to their respective events"""
        self.actionDebug.triggered.connect(self.event_debug)
        self.actionEnglish.triggered.connect(lambda: self.set_language("en"))
        self.actionSpanish.triggered.connect(lambda: self.set_language("es"))
        self.actionExit.triggered.connect(QApplication.instance().quit)
        self.actionAbout.triggered.connect(self.event_actionAbout)
        self.actionConfiguration.triggered.connect(
            self.event_actionConfiguration)
        self.actionClear_List.triggered.connect(self.event_actionClearList)
        self.actionHistory.triggered.connect(self.event_actionViewHistory)
        self.btnAddUrl.clicked.connect(self.event_actionAddUrl)
        self.tableMediaContent.doubleClicked.connect(
            self.on_table_double_click)

    def event_debug(self):
        print(self.workers)

    def event_actionAbout(self):
        """Event for the About action"""
        self.raise_info(
            self.dictionary["about"]["text"], self.dictionary["about"]["title"])

    def load_conf(self):
        keys = [
            "path", "filename", "cb_max_downloads", "max_downloads", "type",
            "quality_video", "format_video", "quality_audio", "format_audio",
            "cb_subtitles", "lang_subtitles", "cb_cookies", "cookies",
            "cb_limit_rate", "limit_rate", "cb_proxy", "proxy",
            "cb_thumbnail", "cb_no_overwrites", "cb_metadata",
            "cb_embed_subtitles", "cb_restrict_filename", "cb_no_playlist", "cb_download_archive"
        ]
        default = ["default", "default", "False", "1", "0", "Best", "mp4", "Best", "m4a",
                   "False", "", "False", "", "False", "", "False", "", "False", "False", "False", "False", "False", "False", "False"]

        config_data = {}
        for key in keys:
            try:
                value = get_config_value(
                    "downloader", key, default[keys.index(key)])
                if key.startswith("cb_"):
                    config_data[key] = value in ("True", "true", True)
                else:
                    config_data[key] = value
            except KeyError:
                config_data[key] = None

        return config_data

    def event_actionConfiguration(self):
        """Event for the Configuration action"""
        def save_conf(conf: dict):
            for key, value in conf.items():
                if type(value) in (bool, int):
                    value = str(value)
                set_config_value("downloader", key, value)

        def delete_config_window():
            del self.config_window

        if not hasattr(self, 'config_window'):
            conf = self.load_conf()
            self.config_window = ConfigWindow(window, self.lang, conf)
            self.config_window.save_signal.connect(
                lambda conf: save_conf(conf))
            self.config_window.cancel_signal.connect(delete_config_window)

        elif not self.config_window.isVisible():
            self.config_window.reload_language(self.lang)
            self.config_window.show()
        else:
            self.config_window.reload_language(self.lang)
            self.config_window.raise_()
            self.config_window.activateWindow()

    def event_actionAddUrl(self):
        """Event for the Add URL action"""
        # extract info from the ui
        url = self.inputUrl.text()
        if url == "":
            return
        self.inputUrl.setText("")

        conf = self.load_conf()

        worker = DownloadWorker("build", DownloadTask(url, conf))
        self.workers[url] = worker
        worker.signals.finished.connect(lambda: self.pack_worker(url))
        worker.signals.error.connect(
            lambda status: self.discard_worker(url, status))
        self.thread_pool.start(worker)

    def pack_worker(self, url: str):
        worker = self.workers[url]
        items = self.create_table_item(worker.task)
        progress = QProgressBar()
        progress.setTextVisible(False)
        progress.setMinimum(0)
        progress.setMaximum(100)

        # add to QTableView
        self.add_item_to_table(items, progress)

    def discard_worker(self, url: str, status: str):
        if status == "invalid_url":
            self.raise_error(self.dictionary["errors"]["invalid_url"])
        else:
            self.raise_error(self.dictionary["errors"]["extract_info"])
        del self.workers[url]

    def event_actionClearList(self):
        """Event for the Clear List action"""
        reply = QMessageBox.question(
            self,
            self.dictionary["elements"]["item_table"]["delete_question"]["title"],
            self.dictionary["elements"]["item_table"]["delete_question"]["text"],
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.table_model.clear()

            for key in list(self.workers.keys()):
                worker = self.workers.pop(key)
                try:
                    worker.task.cancel()
                    worker.signals.finished.disconnect()
                    worker.signals.error.disconnect()
                    del worker

                except Exception as e:
                    print(f"Error cleaning worker [{key}]:", e)

            self.prepare_table()
            self.set_table_headers()

    def event_actionViewHistory(self):
        """Event for the View History action"""
        def event_actionHistory(action: str):
            if action == "delete":
                """Event for the Clear History action"""
                reply = QMessageBox.question(
                    self,
                    self.dictionary["elements"]["item_table"]["delete_question"]["title"],
                    self.dictionary["elements"]["item_table"]["delete_question"]["text"],
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    log_path = ROOT / "history.log"
                    if log_path.exists():
                        log_path.unlink()
                        self.raise_info(
                            self.dictionary["msg"]["deletedHistory"])
                    else:
                        self.raise_error(
                            self.dictionary["errors"]["deletedHistoryError"])

            elif action == "save":
                """Event for the Save History action"""
                if self.table_model.rowCount() == 0:
                    return

                log_path = ROOT / "history.log"

                with open(log_path, "a", encoding="utf-8") as f:
                    for row in range(self.table_model.rowCount()):
                        progress_widget = self.tableMediaContent.indexWidget(
                            self.table_model.index(row, 3))

                        if progress_widget and progress_widget.value() == 100:
                            status = "::sf::"

                        elif progress_widget and progress_widget.value() > 0:
                            status = f"::si:: {progress_widget.value()} %"

                        title = self.table_model.item(row, 0).text()
                        size = self.table_model.item(row, 2).text()
                        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        f.write(
                            f"{row+1}]::\nx: {status},\ny: {title},\nz: {size},\nd: {date}\n\n")

                self.raise_info(self.dictionary["msg"]["savedHistory"])

        def load_history_file():
            log_path = ROOT / "history.log"

            text = ""

            if log_path.exists():
                with open(log_path, "r", encoding="utf-8") as f:
                    text = f.read()

                base = self.dictionary["elements"]["placeHolders"]["history"]
                text = text.replace("x:", base.get("status") + ":")
                text = text.replace("::sf::", base.get("status_finished"))
                text = text.replace("::si::", base.get("status_interrupted"))
                text = text.replace("y:", base.get("title") + ":")
                text = text.replace("z:", base.get("size") + ":")
                text = text.replace("d:", base.get("date") + ":")

            return text

        if not hasattr(self, 'history_window'):
            self.history_window = HistoryDialog(self.lang, load_history_file())
            self.history_window.actionSignal.connect(event_actionHistory)

        elif not self.history_window.isVisible():
            self.history_window.history = load_history_file()
            self.history_window.reload_language(self.lang)
            self.history_window.show()
        else:
            self.history_window.history = load_history_file()
            self.history_window.reload_language(self.lang)
            self.history_window.raise_()
            self.history_window.activateWindow()

    def toggle_download(self, row: int):
        """Start, pause, or resume a download based on the current status"""
        task = self._get_object_data_from_row(row)
        current_worker = self.workers.get(task.url)
        btn = self.tableMediaContent.indexWidget(
            self.table_model.index(row, 6))

        if not hasattr(task, "retry_count"):
            task.retry_count = 0

        def update_button_success(_):
            task.retry_count = 0  # Restart Attempts
            btn.setText("✅")
            self.workers.pop(task.url, None)

        def update_button_error(_):
            self.workers.pop(task.url, None)
            task.retry_count += 1
            if task.retry_count <= 3:
                print(f"[{task.url}] Retrying... ({task.retry_count}/3)")
                # Try again
                QTimer.singleShot(3000, lambda: self.toggle_download(row))
            else:
                print(f"[{task.url}] Failed after 3 attempts.")
                btn.setText("🔁")

        def assign_events_to_new_worker(new_worker: DownloadWorker):
            # Connect signals to clean up the worker upon completion
            new_worker.signals.finished.connect(update_button_success)
            new_worker.signals.error.connect(update_button_error)

            # Connect the signal to update the UI
            new_worker.signals.progress.connect(
                lambda percent, speed, eta: self.update_progress_ui(task.url, percent, speed, eta))

            return

        # If the button is ✅, we show a successful download message
        if btn.text() == "✅":
            self.raise_info(
                self.dictionary["msg"]["download_success"] + f": {task.url}")
            return

        # If the button is 🔁, we treat it as a retry
        if btn.text() == "🔁":
            task.state = "idle"  # restart it manually
            self.toggle_download(row)
            return

        if task.state == "paused":
            # Resume
            if task.is_running():
                print(f"[{task.url}] Skipping new worker, already running")
                return

            current_worker = self.workers.pop(task.url, None)
            if current_worker and current_worker.task.process:
                try:
                    current_worker.task.process.terminate()
                except Exception as e:
                    print(
                        f"[{task.url}] Error terminating old process: {e}")

            del current_worker

            new_worker = DownloadWorker("resume", task)
            assign_events_to_new_worker(new_worker)
            self.workers[task.url] = new_worker
            self.thread_pool.start(new_worker)

            print(f"[{task.url}] resuming download...")
            btn.setText("⏸️")

        elif task.state == "downloading":
            # Pause
            if task.process and task.process.poll() is None:
                print(f"[{task.url}] pausing download...")
                task.pause()
                btn.setText("▶️")

        elif task.state in ("idle", "completed", "cancelled"):
            # Discharge
            print(f"[{task.url}] starting download...")
            new_worker = DownloadWorker("download", task)

            assign_events_to_new_worker(new_worker)

            self.workers[task.url] = new_worker
            self.thread_pool.start(new_worker)
            btn.setText("⏸️")

        else:
            print(f"[{task.url}] unknown status: {task.state}")

    def update_progress_ui(self, url: str, percent: int, speed: str, eta: str):
        row = self._get_row_from_url(url)

        if row == -1:
            print(f"Row not found for URL: {url}")
            return

        # get the progress bar from column 3
        progress_bar = self.tableMediaContent.indexWidget(
            self.table_model.index(row, 3))

        if isinstance(progress_bar, QProgressBar):
            progress_bar.setValue(percent)
        else:
            print("QProgressBar not found in row", row)

        self.table_model.setData(self.table_model.index(row, 4), speed)
        self.table_model.setData(self.table_model.index(row, 5), eta)

    def on_table_double_click(self, index):
        """Event for the double click on the table"""
        row = index.row()

        title_item = self.table_model.item(row, 0)
        title = title_item.text() if title_item else "Untitled"

        reply = QMessageBox.question(
            self,
            self.dictionary["elements"]["item_table"]["delete_question"]["title"],
            self.dictionary["elements"]["item_table"]["delete_question"]["text"] +
            f"\n\t{row+1}) {title}",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            task = self._get_object_data_from_row(row)

            # Try canceling if downloading
            if task and task.state == "downloading":
                print(
                    f"[{task.url}] Canceling download before deleting row...")
                task.cancel()

                # You can also terminate the process if it exists
                worker = self.workers.get(task.url)
                if worker and task.process:
                    try:
                        task.process.terminate()
                        print(
                            f"[{task.url}] Process completed successfully")
                    except Exception as e:
                        print(
                            f"[{task.url}] Error terminating the process: {e}")

                # Remove the worker from the dictionary
                self.workers.pop(task.url, None)

            # Delete the row from the table
            self.table_model.removeRow(row)

    def create_table_item(self, data_object: DownloadTask) -> list[QStandardItem]:
        """Create a table item with the given data"""
        item_title = QStandardItem(data_object.metadata.get("title"))
        item_title.setData(data_object, Qt.UserRole)

        item_duration = QStandardItem(data_object.metadata.get("duration"))
        item_size = QStandardItem(data_object.metadata.get("filesize"))
        item_progress = QStandardItem("")
        item_speed = QStandardItem("")
        item_time = QStandardItem("00:00")
        item_btn_action = QStandardItem("")

        for item in [item_duration, item_size, item_progress, item_speed, item_time]:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        return [item_title, item_duration, item_size, item_progress, item_speed, item_time, item_btn_action]

    def add_item_to_table(self, items: list[QStandardItem], progress: QProgressBar) -> None:
        """Add an item to the table"""
        row = self.table_model.rowCount()
        self.table_model.appendRow(items)

        # Add the progress bar to the table
        self.tableMediaContent.setIndexWidget(
            self.table_model.index(row, 3), progress)  # Column 3 = progress
        # Add thumbnail
        url = self._get_object_data_from_row(row).metadata.get("thumbnail")
        self.load_thumbnail(url, row)

        # Add start/pause button
        btn = QPushButton("▶️")  # Start icon
        btn.setFixedSize(50, 30)
        btn.clicked.connect(lambda _, r=row: self.toggle_download(r))
        self.tableMediaContent.setIndexWidget(
            # Assuming column 6 is the button
            self.table_model.index(row, 6), btn)

    def load_thumbnail(self, url: str, row: int):
        loader = ThumbnailLoader(url, row)
        loader.finished.connect(self.on_thumbnail_loaded)
        # Clean the thread when it ends
        loader.finished.connect(loader.deleteLater)
        loader.start()

        self.thumbnail_threads.append(loader)  # Save reference

    def on_thumbnail_loaded(self, pixmap: QPixmap, row: int):
        if not pixmap.isNull():
            item = self.table_model.item(row, 0)
            item.setIcon(QIcon(pixmap))

        # Remove finished thread
        self.thumbnail_threads = [
            t for t in self.thumbnail_threads if t.isRunning()
        ]

    def _get_object_data_from_row(self, row: int) -> DownloadTask | None:
        """Get the object data from the table"""
        item = self.table_model.item(row, 0)
        return item.data(Qt.UserRole) if item else None

    def _get_row_from_url(self, url: str) -> int:
        """Returns the row number that contains the given URL, or -1 if not found."""
        for row in range(self.table_model.rowCount()):
            task: DownloadTask = self.table_model.data(
                self.table_model.index(row, 0), Qt.UserRole)
            if task.url == url:
                return row
        return -1

    def raise_info(self, info: str, title: str = "Info"):
        """Raise an info message"""
        QMessageBox.information(self, title, info)
        return

    def raise_error(self, error: str, title: str = "Error"):
        """Raise an error message"""
        QMessageBox.critical(self, title, error)
        return


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
