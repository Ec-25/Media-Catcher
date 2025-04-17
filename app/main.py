from datetime import datetime
from pathlib import Path
from sys import exit as sys_exit, argv as sys_argv
from configparser import ConfigParser

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QProgressBar, QPushButton, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon, QAction
from PySide6.QtCore import QCoreApplication, QEvent

from packages import LoadingDialog, check_dependencies, check_packages, download_missing, write_debug_log
from downloader import ConfigWindow, DownloadManager, ThumbnailLoader, DownloadTask, DownloadWorker

from gui.main import Ui_MainWindow
from gui.history import Ui_History

from translations import translations


class HistoryDialog(QDialog, Ui_History):
    actionSignal = Signal(str)

    def __init__(self, parent, lang: str, history: str):
        super().__init__(parent=parent)
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
        self.setupUi(self)
        self.awaitLoad()
        self.init_language()
        self.connectEvents()
        self.show()

    # Ui Start
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.close_all.emit()
                self.hide()
                self.tray_icon.showMessage(
                    self.dictionary["title"],
                    self.dictionary["msg"]["background_application"],
                    QSystemTrayIcon.Information,
                    3000
                )

        super().changeEvent(event)

    def closeEvent(self, event):
        if self.table_model.rowCount() != 0 and self.download_manager.active_downloads != 0:
            reply = QMessageBox.question(
                self,
                self.dictionary["msg"]["exit_title"],
                self.dictionary["msg"]["exit_text"],
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

            self.cancel_downloads()

            if self.debug:
                msg = "List cleaned successfully"
                write_debug_log(msg)

        if self.debug:
            write_debug_log("Closing application")

        self.close_all.emit()
        event.accept()

    def awaitLoad(self):
        """Load all essential content"""
        def prepare_table():
            self.table_model = QStandardItemModel()
            self.table_model.setColumnCount(10)

            self.tableMediaContent.setModel(self.table_model)
            self.tableMediaContent.setColumnWidth(0, 400)  # title
            self.tableMediaContent.setColumnWidth(1, 80)  # type
            self.tableMediaContent.setColumnWidth(2, 80)  # quality
            self.tableMediaContent.setColumnWidth(3, 100)  # duration
            self.tableMediaContent.setColumnWidth(4, 80)  # ext
            self.tableMediaContent.setColumnWidth(5, 100)  # file size
            self.tableMediaContent.setColumnWidth(6, 300)  # progress bar
            self.tableMediaContent.setColumnWidth(7, 100)  # speed
            self.tableMediaContent.setColumnWidth(8, 80)  # time remaining
            self.tableMediaContent.setColumnWidth(9, 50)  # btn action
            self.tableMediaContent.setIconSize(QSize(53, 42))
            self.tableMediaContent.horizontalHeader().setVisible(True)

        # set language
        self.lang = get_config_value("general", "lang", "en")
        self.dictionary = translations[self.lang]

        # set debug
        self.debug = get_config_value("general", "debug", "False") == "True"
        self.actionDebug.setVisible(self.debug)
        self.actionDebug.setEnabled(self.debug)

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
        prepare_table()

        # resize the main window
        w = 1407
        h = 700
        self.resize(w, h)

        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(
            QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaOptical)), parent=self)
        self.tray_icon.setToolTip(self.dictionary["title"])

        # Tray menu
        tray_menu = QMenu()
        self.show_action = QAction("switch", self)
        self.show_action.triggered.connect(self.event_on_tray_switch)
        tray_menu.addAction(self.show_action)

        self.exit_action = QAction("exit", self)
        self.exit_action.triggered.connect(self.event_on_tray_exit)
        tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setVisible(True)

        # downloader elements
        if get_config_value("downloader", "cb_max_downloads", "True") == "True":
            # apply limit to downloads
            max_downloads = get_config_value(
                "downloader", "max_downloads", "3")
        else:
            # download without limits
            max_downloads = "0"
        self.download_manager = DownloadManager(int(max_downloads))
        self.load_manager = DownloadManager(int(max_downloads))
        self.workers = {}  # key: url, value: DownloadWorker
        self.progress_callbacks = {}
        self.thumbnail_threads = []

    def init_language(self):
        """Initialize the language of the application"""
        def set_table_headers():
            self.table_model.setHorizontalHeaderLabels(
                [self.dictionary["elements"]["table_model"]["title"], self.dictionary["elements"]["table_model"]["type"], self.dictionary["elements"]["table_model"]["quality"], self.dictionary["elements"]["table_model"]["duration"], self.dictionary["elements"]["table_model"]["ext"], self.dictionary["elements"]["table_model"]["size"], self.dictionary["elements"]["table_model"]["downloaded"], self.dictionary["elements"]["table_model"]["speed"], self.dictionary["elements"]["table_model"]["time_remaining"], self.dictionary["elements"]["table_model"]["action"]])
            return

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
        self.menuDownloads.setTitle(self.dictionary["menu"]["downloads"])
        self.menuHelp.setTitle(self.dictionary["menu"]["help"])
        self.menuLanguage.setTitle(self.dictionary["menu"]["language"])

        # menu actions
        self.actionExit.setText(self.dictionary["menuActions"]["exit"])
        self.actionHistory.setText(
            self.dictionary["menuActions"]["history"])
        self.actionConfiguration.setText(
            self.dictionary["menuActions"]["configuration"])
        self.actionDownload_All.setText(
            self.dictionary["menuActions"]["downloadAll"])
        self.actionClear_List.setText(
            self.dictionary["menuActions"]["clearList"])
        self.actionAbout.setText(self.dictionary["menuActions"]["about"])

        # ui elements
        self.inputUrl.setPlaceholderText(
            self.dictionary["elements"]["placeHolders"]["inputUrl"])
        self.btnAddUrl.setText(self.dictionary["elements"]["buttons"]["add"])

        set_table_headers()

        # tray menu
        self.show_action.setText(self.dictionary["menuActions"]["switch"])
        self.exit_action.setText(self.dictionary["menuActions"]["exit"])

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

    def raise_message(self, type_msg: str, title: str, text: str):
        def info():
            """Raise an info message"""
            QMessageBox.information(self, title, text)
            return

        def warning():
            """Raise a warning message"""
            QMessageBox.warning(self, title, text)
            return

        def error():
            """Raise an error message"""
            QMessageBox.critical(self, title, text)
            return

        match type_msg:
            case "info":
                info()
            case "error":
                error()
            case _:
                warning()
        return

    def get_object_data_from_row(self, row: int) -> DownloadTask | None:
        """Get the object data from the table"""
        item = self.table_model.item(row, 0)
        return item.data(Qt.UserRole) if item else None

    # Ui Events
    def connectEvents(self):
        """Connect all senders to their respective events"""
        self.tray_icon.activated.connect(self.event_on_tray_activated)
        self.actionDebug.triggered.connect(self.event_debug)
        self.actionEnglish.triggered.connect(
            lambda: self.event_set_language("en"))
        self.actionSpanish.triggered.connect(
            lambda: self.event_set_language("es"))
        self.actionExit.triggered.connect(QApplication.instance().quit)
        self.actionAbout.triggered.connect(self.event_actionAbout)
        self.actionConfiguration.triggered.connect(
            self.event_actionConfiguration)
        self.actionDownload_All.triggered.connect(self.event_actionDownloadAll)
        self.actionClear_List.triggered.connect(self.event_actionClearList)
        self.actionHistory.triggered.connect(self.event_actionViewHistory)
        self.btnAddUrl.clicked.connect(self.event_actionAddUrl)
        self.tableMediaContent.doubleClicked.connect(
            self.event_on_table_double_click)

    def event_on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def event_on_tray_switch(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def event_on_tray_exit(self):
        self.show()
        QCoreApplication.quit()

    def event_set_language(self, lang):
        # set the language in the application and in the settings
        self.lang = lang
        set_config_value("general", "lang", lang)
        self.dictionary = translations[lang]

        self.init_language()

    def event_debug(self):
        if self.debug:
            msg = self.workers
            write_debug_log(msg)
            print(msg)

    def event_actionAbout(self):
        """Event for the About action"""
        self.raise_message("info",
                           self.dictionary["about"]["title"], self.dictionary["about"]["text"])

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
            self.config_window = ConfigWindow(self, self.lang, conf)
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

        self.create_download(url, conf)
        return

    def event_actionDownloadAll(self):
        """Event for the Download All action"""
        if self.table_model.rowCount() == 0:
            return

        for row in range(self.table_model.rowCount()):
            if self.table_model.item(row, 6).text() == "100 %":
                continue

            self.event_toggle_download(row)

    def event_actionClearList(self):
        """Event for the Clear List action"""
        reply = QMessageBox.question(
            self,
            self.dictionary["elements"]["item_table"]["delete_question"]["title"],
            self.dictionary["elements"]["item_table"]["delete_question"]["text"],
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.cancel_downloads()

            if self.debug:
                msg = "List cleaned successfully"
                write_debug_log(msg)

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
                        self.raise_message("info", "Info",
                                           self.dictionary["msg"]["deletedHistory"])
                    else:
                        self.raise_message("error", "Error",
                                           self.dictionary["errors"]["deletedHistoryError"])

            elif action == "save":
                """Event for the Save History action"""
                if self.table_model.rowCount() == 0:
                    return

                log_path = ROOT / "history.log"

                with open(log_path, "a", encoding="utf-8") as f:
                    for row in range(self.table_model.rowCount()):
                        progress_widget = self.tableMediaContent.indexWidget(
                            self.table_model.index(row, 6))

                        if progress_widget and progress_widget.value() == 100:
                            status = "::sf::"

                        elif progress_widget and progress_widget.value() >= 0:
                            status = f"::si:: {progress_widget.value()} %"

                        else:
                            status = "::sni::"

                        title = self.table_model.item(row, 0).text()
                        size = self.table_model.item(row, 5).text()
                        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        f.write(
                            f"{row+1}]::\nx: {status},\ny: {title},\nz: {size},\nd: {date}\n\n")

                self.raise_message(
                    "info", "Info", self.dictionary["msg"]["savedHistory"])

            self.history_window.close()

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
                text = text.replace(
                    "::sni::", base.get("status_not_initialized"))
                text = text.replace("y:", base.get("title") + ":")
                text = text.replace("z:", base.get("size") + ":")
                text = text.replace("d:", base.get("date") + ":")

            return text

        if not hasattr(self, 'history_window'):
            self.history_window = HistoryDialog(
                self, self.lang, load_history_file())
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

    def event_on_table_double_click(self, index):
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
            self.cancel_download(row)

    def event_toggle_download(self, row: int):
        """Start, pause, or resume a download based on the current status"""
        task = self.get_object_data_from_row(row)
        btn = self.tableMediaContent.indexWidget(
            self.table_model.index(row, 9))

        if not hasattr(task, "retry_count"):
            task.retry_count = 0

        if btn.text() in ("▶️", "⏸️"):
            if task.state == "paused":
                # Resume
                self.run_download(row, task, btn, "resume")
                return

            elif task.state == "downloading":
                # Pause
                self.pause_download(task, btn)
                return

            elif task.state == "idle":
                # Run
                self.run_download(row, task, btn)
                return

            else:
                # Error
                if self.debug:
                    msg = f"[{task.url}] unknown status: {task.state}"
                    write_debug_log(msg)
                return

        elif btn.text() == "⏳":
            # If the button is ⏳, we treat it as a pause
            btn.setText("▶️")
            self.pause_download(task, btn)
            return

        elif btn.text() == "✅":
            # If the button is ✅, we show a successful download message
            title = "Info"
            text = f"{self.dictionary["msg"]["download_success"]}: {task.url}"
            self.raise_message("info", title, text)
            return

        elif btn.text() == "❌":
            title = "Error"
            text = f"{self.dictionary["errors"]["download_error"]}: {task.url}"
            self.raise_message("error", title, text)
            return

        elif btn.text() == "🔁":
            # If the button is 🔁, we treat it as a retry
            btn.setText("⏳")
            task.state = "idle"  # restart it manually
            QTimer.singleShot(1000, lambda: self.event_toggle_download(row))
            return

        else:
            # Error
            if self.debug:
                msg = f"[{task.url}] unknown status: {task.state}"
                write_debug_log(msg)
            return

    # Download Manipulation
    def create_download(self, url: str, conf: dict):
        def load_thumbnail(url: str, row: int):
            def on_thumbnail_loaded(pixmap: QPixmap, row: int):
                if not pixmap.isNull():
                    item = self.table_model.item(row, 0)
                    item.setIcon(QIcon(pixmap))

                # Remove finished thread
                self.thumbnail_threads = [
                    t for t in self.thumbnail_threads if t.isRunning()
                ]

            loader = ThumbnailLoader(url, row)
            loader.finished.connect(on_thumbnail_loaded)
            # Clean the thread when it ends
            loader.finished.connect(loader.deleteLater)
            loader.start()

            self.thumbnail_threads.append(loader)  # Save reference

        def create_table_item(data_object: DownloadTask) -> list[QStandardItem]:
            """Create a table item with the given data"""
            item_title = QStandardItem(data_object.metadata.get("title"))
            item_title.setData(data_object, Qt.UserRole)
            item_type = QStandardItem(data_object.output_data.get("type"))
            item_quality = QStandardItem(
                data_object.output_data.get("quality"))
            duration = data_object.metadata.get("duration")
            if not duration:
                duration = self.dictionary.get("errors").get("unknown")
            item_duration = QStandardItem(duration)
            item_ext = QStandardItem(data_object.output_data.get("ext"))
            filesize = data_object.metadata.get("filesize")
            if not filesize:
                filesize = self.dictionary.get("errors").get("unknown")
            item_size = QStandardItem(filesize)
            item_progress = QStandardItem("")
            item_speed = QStandardItem("")
            item_time = QStandardItem("")
            item_btn_action = QStandardItem("")

            for item in [item_duration, item_ext, item_size, item_progress, item_speed, item_time]:
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            return [item_title, item_type, item_quality, item_duration, item_ext, item_size, item_progress, item_speed, item_time, item_btn_action]

        def add_item_to_table(items: list[QStandardItem], progress: QProgressBar):
            """Add an item to the table"""
            row = self.table_model.rowCount()
            self.table_model.appendRow(items)

            # Add the progress bar to the table
            self.tableMediaContent.setIndexWidget(
                # Column 6 = progress
                self.table_model.index(row, 6), progress)
            # Add thumbnail
            url = self.get_object_data_from_row(row).metadata.get("thumbnail")
            load_thumbnail(url, row)

            # Add start/pause button
            btn = QPushButton("▶️")  # Start icon
            btn.setFixedSize(50, 30)
            btn.clicked.connect(lambda _, r=row: self.event_toggle_download(r))
            self.tableMediaContent.setIndexWidget(
                # Assuming column 9 is the button
                self.table_model.index(row, 9), btn)
            return

        def pack_worker(worker: DownloadWorker):
            items = create_table_item(worker.task)
            progress = QProgressBar()
            progress.setTextVisible(False)
            progress.setMinimum(0)
            progress.setMaximum(100)

            # add to QTableView
            add_item_to_table(items, progress)
            return

        def discard_worker(url: str, status: str):
            if status == "invalid_url":
                self.raise_message(
                    "error", "Error", self.dictionary["errors"]["invalid_url"])
            else:
                self.raise_message(
                    "error", "Error", self.dictionary["errors"]["extract_info"])
            del self.workers[url]
            return

        # create object
        task = DownloadTask(url, self.debug, conf)
        worker = DownloadWorker("build", task, self.debug)
        self.workers[url] = worker

        # initialize in ui
        worker.signals.finished.connect(
            lambda: pack_worker(worker))
        worker.signals.error.connect(
            lambda status: discard_worker(url, status))

        if worker.mode != "build":
            worker.mode = "build"
        self.load_manager.add_download(worker)
        return

    def run_download(self, row: int, task: DownloadTask, btn, type: str = "run"):
        def update_progress_ui(url: str, filesize: str, percent: int, speed: str, eta: str):
            def _get_row_from_url(url: str) -> int:
                """Returns the row number that contains the given URL, or -1 if not found."""
                for row in range(self.table_model.rowCount()):
                    task: DownloadTask = self.table_model.data(
                        self.table_model.index(row, 0), Qt.UserRole)
                    if task.url == url:
                        return row
                return -1

            row = _get_row_from_url(url)

            if row == -1:
                if self.debug:
                    msg = f"Row not found for URL: {url}"
                    write_debug_log(msg)
                return

            if filesize:
                self.table_model.setData(
                    self.table_model.index(row, 5), filesize)

            # get the progress bar from column 6
            progress_bar = self.tableMediaContent.indexWidget(
                self.table_model.index(row, 6))

            if isinstance(progress_bar, QProgressBar):
                progress_bar.setValue(percent)
            else:
                if self.debug:
                    msg = f"QProgressBar not found in row: {row}"
                    write_debug_log(msg)

            self.table_model.setData(self.table_model.index(row, 7), speed)
            self.table_model.setData(self.table_model.index(row, 8), eta)

        def update_button_success(_):
            task.retry_count = 0  # Restart Attempts
            QTimer.singleShot(500, lambda: (
                self.table_model.setData(self.table_model.index(row, 7), ""),
                self.table_model.setData(self.table_model.index(row, 8), "")
            ))
            btn.setText("✅")
            self.workers.pop(task.url, None)
            if not self.isVisible():
                self.tray_icon.showMessage(
                    self.dictionary["msg"]["download_success"],
                    self.dictionary["msg"]["download_success"] +
                    f". URL: {task.url}",
                    QSystemTrayIcon.Information,
                    2000
                )

        def update_button_error(_):
            self.workers.pop(task.url, None)
            task.retry_count += 1
            if task.retry_count <= 3:
                if self.debug:
                    msg = f"[{task.url}] Retrying... ({task.retry_count}/3)"
                    write_debug_log(msg)

                # Try again
                QTimer.singleShot(
                    3000, lambda: self.event_toggle_download(row))
            elif 3 < task.retry_count < 6:
                if self.debug:
                    msg = f"[{task.url}] Failed after {task.retry_count} attempts."
                    write_debug_log(msg)

                btn.setText("🔁")
                if not self.isVisible():
                    self.tray_icon.showMessage(
                        self.dictionary["msg"]["download_paused"],
                        self.dictionary["msg"]["download_paused"] +
                        f". URL: {task.url}",
                        QSystemTrayIcon.Warning,
                        2000
                    )
            else:
                if self.debug:
                    msg = f"[{task.url}] Failed after {task.retry_count} attempts."
                    write_debug_log(msg)

                btn.setText("❌")
                QTimer.singleShot(500, lambda: (
                    self.table_model.setData(
                        self.table_model.index(row, 7), ""),
                    self.table_model.setData(
                        self.table_model.index(row, 8), "")
                ))
                if not self.isVisible():
                    self.tray_icon.showMessage(
                        self.dictionary["errors"]["download_error"],
                        self.dictionary["errors"]["download_error"] +
                        f". URL: {task.url}",
                        QSystemTrayIcon.Critical,
                        2000
                    )

        def assign_events_to_new_worker(new_worker: DownloadWorker):
            # Connect signals to clean up the worker upon completion
            new_worker.signals.finished.connect(update_button_success)
            new_worker.signals.error.connect(update_button_error)

            # Connect the signal to update the UI
            def progress_callback(filesize, percent, speed, eta): return update_progress_ui(
                task.url, filesize, percent, speed, eta)
            self.progress_callbacks[task.url] = progress_callback
            new_worker.signals.progress.connect(progress_callback)
            return

        if type == "run":
            # Start
            if self.debug:
                msg = f"[{task.url}] Starting Download..."
                write_debug_log(msg)

            new_worker = DownloadWorker("download", task, self.debug)
            assign_events_to_new_worker(new_worker)

            self.workers[task.url] = new_worker
            self.download_manager.add_download(new_worker)
            btn.setText("⏸️")
        else:
            # Resume
            if task.is_running():
                if self.debug:
                    msg = f"[{task.url}] Skipping new worker, already running"
                    write_debug_log(msg)
                return

            current_worker = self.workers.pop(task.url, None)
            if current_worker and current_worker.task.process:
                try:
                    current_worker.task.process.terminate()
                except Exception as e:
                    if self.debug:
                        msg = f"[{task.url}] Error terminating old process: {e}"
                        write_debug_log(msg)
                        print(msg)

            del current_worker

            new_worker = DownloadWorker("resume", task, self.debug)
            assign_events_to_new_worker(new_worker)
            self.workers[task.url] = new_worker
            self.download_manager.add_download(new_worker)

            if self.debug:
                msg = f"[{task.url}] resuming download..."
                write_debug_log(msg)

            btn.setText("⏸️")

    def pause_download(self, task: DownloadTask, btn):
        if task.process and task.process.poll() is None:
            if self.debug:
                msg = f"[{task.url}] pausing download..."
                write_debug_log(msg)

            task.pause()
            btn.setText("▶️")

    def cancel_download(self, row: int):
        task = self.get_object_data_from_row(row)

        # Try canceling if downloading
        if task and task.state == "downloading":
            task.cancel()

        if not task:
            return

        # Remove the worker from the dictionary
        worker = self.workers.pop(task.url, None)
        if worker:
            # Disconnect signals to avoid any stray calls
            try:
                worker.task.state = "cancelled"
                worker.task.pause()  # in case it is active
                worker.signals.finished.disconnect()
                worker.signals.error.disconnect()
                callback = self.progress_callbacks.pop(task.url, None)
                if callback:
                    worker.signals.progress.disconnect(callback)
            except TypeError:
                # They were already disconnected or not connected yet
                pass

            if worker.task.process and worker.task.process.poll() is None:
                try:
                    worker.task.process.terminate()
                except Exception as e:
                    if self.debug:
                        msg = f"[{task.url}] Error terminating process: {e}"
                        write_debug_log(msg)
                        print(msg)

        # Delete the row from the table
        del worker
        self.table_model.removeRow(row)

        if self.debug:
            msg = f"[{task.url}] Row deleted"
            write_debug_log(msg)

    def cancel_downloads(self):
        total_rows = self.table_model.rowCount()
        if total_rows == 0:
            return

        for row in reversed(range(total_rows)):
            self.cancel_download(row)


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
