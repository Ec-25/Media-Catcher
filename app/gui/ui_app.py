# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QToolButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 640)
        icon = QIcon(QIcon.fromTheme(u"media-optical"))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setPointSize(9)
        self.centralwidget.setFont(font)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gb_status = QGroupBox(self.centralwidget)
        self.gb_status.setObjectName(u"gb_status")
        self.gridLayout_3 = QGridLayout(self.gb_status)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tw = QTreeWidget(self.gb_status)
        __qtreewidgetitem = QTreeWidgetItem()
        self.tw.setHeaderItem(__qtreewidgetitem)
        self.tw.setObjectName(u"tw")
        self.tw.header().setVisible(True)

        self.gridLayout_3.addWidget(self.tw, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.gb_status, 1, 0, 1, 3)

        self.gb_controls = QGroupBox(self.centralwidget)
        self.gb_controls.setObjectName(u"gb_controls")
        self.verticalLayout_2 = QVBoxLayout(self.gb_controls)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pb_add = QPushButton(self.gb_controls)
        self.pb_add.setObjectName(u"pb_add")
        icon1 = QIcon(QIcon.fromTheme(u"list-add"))
        self.pb_add.setIcon(icon1)
        self.pb_add.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.pb_add)

        self.pb_clear = QPushButton(self.gb_controls)
        self.pb_clear.setObjectName(u"pb_clear")
        icon2 = QIcon(QIcon.fromTheme(u"edit-delete"))
        self.pb_clear.setIcon(icon2)
        self.pb_clear.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.pb_clear)

        self.pb_download = QPushButton(self.gb_controls)
        self.pb_download.setObjectName(u"pb_download")
        icon3 = QIcon(QIcon.fromTheme(u"emblem-downloads"))
        self.pb_download.setIcon(icon3)
        self.pb_download.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.pb_download)


        self.gridLayout.addWidget(self.gb_controls, 0, 2, 1, 1)

        self.gb_embeds = QGroupBox(self.centralwidget)
        self.gb_embeds.setObjectName(u"gb_embeds")
        self.gb_embeds.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gb_embeds.setFlat(False)
        self.gb_embeds.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.gb_embeds)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lb_faudio = QLabel(self.gb_embeds)
        self.lb_faudio.setObjectName(u"lb_faudio")

        self.gridLayout_2.addWidget(self.lb_faudio, 2, 2, 1, 1)

        self.le_subtitles = QLineEdit(self.gb_embeds)
        self.le_subtitles.setObjectName(u"le_subtitles")
        self.le_subtitles.setEnabled(False)

        self.gridLayout_2.addWidget(self.le_subtitles, 0, 3, 1, 1)

        self.ob_qvideo = QComboBox(self.gb_embeds)
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.addItem("")
        self.ob_qvideo.setObjectName(u"ob_qvideo")

        self.gridLayout_2.addWidget(self.ob_qvideo, 1, 1, 1, 1)

        self.lb_fvideo = QLabel(self.gb_embeds)
        self.lb_fvideo.setObjectName(u"lb_fvideo")

        self.gridLayout_2.addWidget(self.lb_fvideo, 2, 0, 1, 1)

        self.cb_subtitles = QCheckBox(self.gb_embeds)
        self.cb_subtitles.setObjectName(u"cb_subtitles")

        self.gridLayout_2.addWidget(self.cb_subtitles, 0, 2, 1, 1)

        self.ob_qaudio = QComboBox(self.gb_embeds)
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.addItem("")
        self.ob_qaudio.setObjectName(u"ob_qaudio")

        self.gridLayout_2.addWidget(self.ob_qaudio, 1, 3, 1, 1)

        self.ob_type = QComboBox(self.gb_embeds)
        self.ob_type.addItem("")
        self.ob_type.addItem("")
        self.ob_type.setObjectName(u"ob_type")

        self.gridLayout_2.addWidget(self.ob_type, 0, 1, 1, 1)

        self.lb_qvideo = QLabel(self.gb_embeds)
        self.lb_qvideo.setObjectName(u"lb_qvideo")

        self.gridLayout_2.addWidget(self.lb_qvideo, 1, 0, 1, 1)

        self.lb_qaudio = QLabel(self.gb_embeds)
        self.lb_qaudio.setObjectName(u"lb_qaudio")

        self.gridLayout_2.addWidget(self.lb_qaudio, 1, 2, 1, 1)

        self.ob_fvideo = QComboBox(self.gb_embeds)
        self.ob_fvideo.addItem("")
        self.ob_fvideo.addItem("")
        self.ob_fvideo.addItem("")
        self.ob_fvideo.addItem("")
        self.ob_fvideo.addItem("")
        self.ob_fvideo.setObjectName(u"ob_fvideo")

        self.gridLayout_2.addWidget(self.ob_fvideo, 2, 1, 1, 1)

        self.ob_faudio = QComboBox(self.gb_embeds)
        self.ob_faudio.addItem("")
        self.ob_faudio.addItem("")
        self.ob_faudio.addItem("")
        self.ob_faudio.addItem("")
        self.ob_faudio.setObjectName(u"ob_faudio")

        self.gridLayout_2.addWidget(self.ob_faudio, 2, 3, 1, 1)

        self.lb_type = QLabel(self.gb_embeds)
        self.lb_type.setObjectName(u"lb_type")

        self.gridLayout_2.addWidget(self.lb_type, 0, 0, 1, 1)

        self.cb_metadata = QCheckBox(self.gb_embeds)
        self.cb_metadata.setObjectName(u"cb_metadata")

        self.gridLayout_2.addWidget(self.cb_metadata, 0, 4, 1, 1)

        self.cb_thumbnail = QCheckBox(self.gb_embeds)
        self.cb_thumbnail.setObjectName(u"cb_thumbnail")

        self.gridLayout_2.addWidget(self.cb_thumbnail, 1, 4, 1, 1)

        self.cb_noplaylist = QCheckBox(self.gb_embeds)
        self.cb_noplaylist.setObjectName(u"cb_noplaylist")

        self.gridLayout_2.addWidget(self.cb_noplaylist, 2, 4, 1, 1)


        self.gridLayout.addWidget(self.gb_embeds, 0, 1, 1, 1)

        self.gb_args = QGroupBox(self.centralwidget)
        self.gb_args.setObjectName(u"gb_args")
        self.gridLayout_4 = QGridLayout(self.gb_args)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.le_url = QLineEdit(self.gb_args)
        self.le_url.setObjectName(u"le_url")
        self.le_url.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.le_url, 1, 1, 1, 3)

        self.le_path = QLineEdit(self.gb_args)
        self.le_path.setObjectName(u"le_path")
        self.le_path.setEnabled(False)
        self.le_path.setReadOnly(False)

        self.gridLayout_4.addWidget(self.le_path, 3, 1, 1, 2)

        self.lb_filename = QLabel(self.gb_args)
        self.lb_filename.setObjectName(u"lb_filename")

        self.gridLayout_4.addWidget(self.lb_filename, 2, 0, 1, 1)

        self.lb_url = QLabel(self.gb_args)
        self.lb_url.setObjectName(u"lb_url")
        self.lb_url.setMinimumSize(QSize(0, 0))

        self.gridLayout_4.addWidget(self.lb_url, 1, 0, 1, 1)

        self.lb_path = QLabel(self.gb_args)
        self.lb_path.setObjectName(u"lb_path")
        self.lb_path.setMinimumSize(QSize(0, 0))

        self.gridLayout_4.addWidget(self.lb_path, 3, 0, 1, 1)

        self.tb_path = QToolButton(self.gb_args)
        self.tb_path.setObjectName(u"tb_path")
        icon4 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.tb_path.setIcon(icon4)

        self.gridLayout_4.addWidget(self.tb_path, 3, 3, 1, 1)

        self.le_filename = QLineEdit(self.gb_args)
        self.le_filename.setObjectName(u"le_filename")

        self.gridLayout_4.addWidget(self.le_filename, 2, 1, 1, 1)

        self.tb_filename = QToolButton(self.gb_args)
        self.tb_filename.setObjectName(u"tb_filename")
        icon5 = QIcon(QIcon.fromTheme(u"edit-undo"))
        self.tb_filename.setIcon(icon5)

        self.gridLayout_4.addWidget(self.tb_filename, 2, 3, 1, 1)


        self.gridLayout.addWidget(self.gb_args, 0, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.cb_subtitles.toggled.connect(self.le_subtitles.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Media-Catcher", None))
        self.gb_status.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        ___qtreewidgetitem = self.tw.headerItem()
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("MainWindow", u"ETA", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"Speed", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Progress", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Format", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Title", None));
        self.gb_controls.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
#if QT_CONFIG(tooltip)
        self.pb_add.setToolTip(QCoreApplication.translate("MainWindow", u"\n"
"                      <html><head/><body><p>Add</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_add.setText("")
#if QT_CONFIG(tooltip)
        self.pb_clear.setToolTip(QCoreApplication.translate("MainWindow", u"\n"
"                      <html><head/><body><p>Clear</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_clear.setText("")
#if QT_CONFIG(tooltip)
        self.pb_download.setToolTip(QCoreApplication.translate("MainWindow", u"\n"
"                      <html><head/><body><p>Download</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_download.setText("")
        self.gb_embeds.setTitle(QCoreApplication.translate("MainWindow", u"Optional", None))
        self.lb_faudio.setText(QCoreApplication.translate("MainWindow", u"Format Audio", None))
        self.le_subtitles.setPlaceholderText(QCoreApplication.translate("MainWindow", u"en, es", None))
        self.ob_qvideo.setItemText(0, QCoreApplication.translate("MainWindow", u"Best", None))
        self.ob_qvideo.setItemText(1, QCoreApplication.translate("MainWindow", u"Worst", None))
        self.ob_qvideo.setItemText(2, QCoreApplication.translate("MainWindow", u"360p", None))
        self.ob_qvideo.setItemText(3, QCoreApplication.translate("MainWindow", u"480p", None))
        self.ob_qvideo.setItemText(4, QCoreApplication.translate("MainWindow", u"720p", None))
        self.ob_qvideo.setItemText(5, QCoreApplication.translate("MainWindow", u"1080p", None))
        self.ob_qvideo.setItemText(6, QCoreApplication.translate("MainWindow", u"1440p", None))
        self.ob_qvideo.setItemText(7, QCoreApplication.translate("MainWindow", u"2160p", None))

        self.lb_fvideo.setText(QCoreApplication.translate("MainWindow", u"Format Video", None))
        self.cb_subtitles.setText(QCoreApplication.translate("MainWindow", u"Subtitles", None))
        self.ob_qaudio.setItemText(0, QCoreApplication.translate("MainWindow", u"Best", None))
        self.ob_qaudio.setItemText(1, QCoreApplication.translate("MainWindow", u"Worst", None))
        self.ob_qaudio.setItemText(2, QCoreApplication.translate("MainWindow", u"64k", None))
        self.ob_qaudio.setItemText(3, QCoreApplication.translate("MainWindow", u"96k", None))
        self.ob_qaudio.setItemText(4, QCoreApplication.translate("MainWindow", u"128k", None))
        self.ob_qaudio.setItemText(5, QCoreApplication.translate("MainWindow", u"192k", None))
        self.ob_qaudio.setItemText(6, QCoreApplication.translate("MainWindow", u"256k", None))
        self.ob_qaudio.setItemText(7, QCoreApplication.translate("MainWindow", u"320k", None))

        self.ob_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Video", None))
        self.ob_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Audio", None))

        self.lb_qvideo.setText(QCoreApplication.translate("MainWindow", u"Quality Video", None))
        self.lb_qaudio.setText(QCoreApplication.translate("MainWindow", u"Quality Audio", None))
        self.ob_fvideo.setItemText(0, QCoreApplication.translate("MainWindow", u"m4v", None))
        self.ob_fvideo.setItemText(1, QCoreApplication.translate("MainWindow", u"mp4", None))
        self.ob_fvideo.setItemText(2, QCoreApplication.translate("MainWindow", u"mov", None))
        self.ob_fvideo.setItemText(3, QCoreApplication.translate("MainWindow", u"mkv", None))
        self.ob_fvideo.setItemText(4, QCoreApplication.translate("MainWindow", u"mka", None))

        self.ob_faudio.setItemText(0, QCoreApplication.translate("MainWindow", u"m4a", None))
        self.ob_faudio.setItemText(1, QCoreApplication.translate("MainWindow", u"mp3", None))
        self.ob_faudio.setItemText(2, QCoreApplication.translate("MainWindow", u"opus", None))
        self.ob_faudio.setItemText(3, QCoreApplication.translate("MainWindow", u"flac", None))

        self.lb_type.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.cb_metadata.setText(QCoreApplication.translate("MainWindow", u"Metadata", None))
        self.cb_thumbnail.setText(QCoreApplication.translate("MainWindow", u"Thumbnail", None))
        self.cb_noplaylist.setText(QCoreApplication.translate("MainWindow", u"NoPlaylist", None))
        self.gb_args.setTitle(QCoreApplication.translate("MainWindow", u"Arguments", None))
        self.le_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"https://www.youtube.com/watch?v=", None))
        self.le_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"~\\Downloads", None))
        self.lb_filename.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
        self.lb_url.setText(QCoreApplication.translate("MainWindow", u"Url", None))
        self.lb_path.setText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.le_filename.setPlaceholderText(QCoreApplication.translate("MainWindow", u"%(title)s.%(ext)s", None))
        self.tb_filename.setText("")
    # retranslateUi
