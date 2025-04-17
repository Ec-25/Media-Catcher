# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'configgUJoDj.ui'
##
# Created by: Qt User Interface Compiler version 6.9.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QFormLayout, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QSpinBox, QWidget)


class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.resize(478, 790)
        font = QFont()
        font.setPointSize(11)
        Config.setFont(font)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        Config.setWindowIcon(icon)
        Config.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.gridLayout_2 = QGridLayout(Config)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(12)
        self.lb_filename = QLabel(Config)
        self.lb_filename.setObjectName(u"lb_filename")

        self.gridLayout_3.addWidget(self.lb_filename, 1, 0, 1, 1)

        self.lb_path = QLabel(Config)
        self.lb_path.setObjectName(u"lb_path")

        self.gridLayout_3.addWidget(self.lb_path, 0, 0, 1, 1)

        self.pb_revertFilename = QPushButton(Config)
        self.pb_revertFilename.setObjectName(u"pb_revertFilename")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentRevert))
        self.pb_revertFilename.setIcon(icon1)

        self.gridLayout_3.addWidget(self.pb_revertFilename, 1, 3, 1, 1)

        self.pb_path = QPushButton(Config)
        self.pb_path.setObjectName(u"pb_path")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.pb_path.setIcon(icon2)

        self.gridLayout_3.addWidget(self.pb_path, 0, 3, 1, 1)

        self.le_filename = QLineEdit(Config)
        self.le_filename.setObjectName(u"le_filename")
        self.le_filename.setEnabled(True)

        self.gridLayout_3.addWidget(self.le_filename, 1, 1, 1, 1)

        self.le_path = QLineEdit(Config)
        self.le_path.setObjectName(u"le_path")
        self.le_path.setEnabled(True)

        self.gridLayout_3.addWidget(self.le_path, 0, 1, 1, 1)

        self.cb_cookies = QCheckBox(Config)
        self.cb_cookies.setObjectName(u"cb_cookies")

        self.gridLayout_3.addWidget(self.cb_cookies, 2, 0, 1, 1)

        self.le_cookies = QLineEdit(Config)
        self.le_cookies.setObjectName(u"le_cookies")
        self.le_cookies.setEnabled(False)

        self.gridLayout_3.addWidget(self.le_cookies, 2, 1, 1, 1)

        self.pb_cookies = QPushButton(Config)
        self.pb_cookies.setObjectName(u"pb_cookies")
        self.pb_cookies.setEnabled(False)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.pb_cookies.setIcon(icon3)

        self.gridLayout_3.addWidget(self.pb_cookies, 2, 3, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.line_12 = QFrame(Config)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.Shape.HLine)
        self.line_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_12, 2, 0, 1, 1)

        self.header = QWidget(Config)
        self.header.setObjectName(u"header")
        self.header.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.title = QLabel(self.header)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 24))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.title.setFont(font1)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.title)

        self.gridLayout_2.addWidget(self.header, 0, 0, 1, 2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setVerticalSpacing(12)
        self.lb_type = QLabel(Config)
        self.lb_type.setObjectName(u"lb_type")

        self.formLayout_2.setWidget(
            4, QFormLayout.ItemRole.LabelRole, self.lb_type)

        self.cb_type = QComboBox(Config)
        self.cb_type.addItem("")
        self.cb_type.addItem("")
        self.cb_type.setObjectName(u"cb_type")

        self.formLayout_2.setWidget(
            4, QFormLayout.ItemRole.FieldRole, self.cb_type)

        self.line = QFrame(Config)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            5, QFormLayout.ItemRole.LabelRole, self.line)

        self.line_2 = QFrame(Config)
        self.line_2.setObjectName(u"line_2")
        sizePolicy.setHeightForWidth(
            self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            5, QFormLayout.ItemRole.FieldRole, self.line_2)

        self.lb_qvideo = QLabel(Config)
        self.lb_qvideo.setObjectName(u"lb_qvideo")

        self.formLayout_2.setWidget(
            6, QFormLayout.ItemRole.LabelRole, self.lb_qvideo)

        self.cb_qvideo = QComboBox(Config)
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.addItem("")
        self.cb_qvideo.setObjectName(u"cb_qvideo")

        self.formLayout_2.setWidget(
            6, QFormLayout.ItemRole.FieldRole, self.cb_qvideo)

        self.lb_fvideo = QLabel(Config)
        self.lb_fvideo.setObjectName(u"lb_fvideo")

        self.formLayout_2.setWidget(
            7, QFormLayout.ItemRole.LabelRole, self.lb_fvideo)

        self.cb_fvideo = QComboBox(Config)
        self.cb_fvideo.addItem("")
        self.cb_fvideo.addItem("")
        self.cb_fvideo.addItem("")
        self.cb_fvideo.addItem("")
        self.cb_fvideo.addItem("")
        self.cb_fvideo.addItem("")
        self.cb_fvideo.setObjectName(u"cb_fvideo")

        self.formLayout_2.setWidget(
            7, QFormLayout.ItemRole.FieldRole, self.cb_fvideo)

        self.line_4 = QFrame(Config)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            8, QFormLayout.ItemRole.LabelRole, self.line_4)

        self.line_3 = QFrame(Config)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            8, QFormLayout.ItemRole.FieldRole, self.line_3)

        self.lb_qaudio = QLabel(Config)
        self.lb_qaudio.setObjectName(u"lb_qaudio")

        self.formLayout_2.setWidget(
            9, QFormLayout.ItemRole.LabelRole, self.lb_qaudio)

        self.cb_qaudio = QComboBox(Config)
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.addItem("")
        self.cb_qaudio.setObjectName(u"cb_qaudio")

        self.formLayout_2.setWidget(
            9, QFormLayout.ItemRole.FieldRole, self.cb_qaudio)

        self.lb_faudio = QLabel(Config)
        self.lb_faudio.setObjectName(u"lb_faudio")

        self.formLayout_2.setWidget(
            10, QFormLayout.ItemRole.LabelRole, self.lb_faudio)

        self.cb_faudio = QComboBox(Config)
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.addItem("")
        self.cb_faudio.setObjectName(u"cb_faudio")

        self.formLayout_2.setWidget(
            10, QFormLayout.ItemRole.FieldRole, self.cb_faudio)

        self.line_6 = QFrame(Config)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            11, QFormLayout.ItemRole.LabelRole, self.line_6)

        self.line_5 = QFrame(Config)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            11, QFormLayout.ItemRole.FieldRole, self.line_5)

        self.line_8 = QFrame(Config)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            13, QFormLayout.ItemRole.LabelRole, self.line_8)

        self.line_7 = QFrame(Config)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            13, QFormLayout.ItemRole.FieldRole, self.line_7)

        self.cb_subtitles = QCheckBox(Config)
        self.cb_subtitles.setObjectName(u"cb_subtitles")

        self.formLayout_2.setWidget(
            12, QFormLayout.ItemRole.LabelRole, self.cb_subtitles)

        self.cb_limitRate = QCheckBox(Config)
        self.cb_limitRate.setObjectName(u"cb_limitRate")

        self.formLayout_2.setWidget(
            15, QFormLayout.ItemRole.LabelRole, self.cb_limitRate)

        self.le_limitRate = QLineEdit(Config)
        self.le_limitRate.setObjectName(u"le_limitRate")
        self.le_limitRate.setEnabled(False)

        self.formLayout_2.setWidget(
            15, QFormLayout.ItemRole.FieldRole, self.le_limitRate)

        self.cb_proxy = QCheckBox(Config)
        self.cb_proxy.setObjectName(u"cb_proxy")

        self.formLayout_2.setWidget(
            16, QFormLayout.ItemRole.LabelRole, self.cb_proxy)

        self.le_proxy = QLineEdit(Config)
        self.le_proxy.setObjectName(u"le_proxy")
        self.le_proxy.setEnabled(False)

        self.formLayout_2.setWidget(
            16, QFormLayout.ItemRole.FieldRole, self.le_proxy)

        self.line_9 = QFrame(Config)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            3, QFormLayout.ItemRole.FieldRole, self.line_9)

        self.line_10 = QFrame(Config)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(
            3, QFormLayout.ItemRole.LabelRole, self.line_10)

        self.sb_maxDownloads = QSpinBox(Config)
        self.sb_maxDownloads.setObjectName(u"sb_maxDownloads")
        self.sb_maxDownloads.setEnabled(False)

        self.formLayout_2.setWidget(
            2, QFormLayout.ItemRole.FieldRole, self.sb_maxDownloads)

        self.cb_maxDownloads = QCheckBox(Config)
        self.cb_maxDownloads.setObjectName(u"cb_maxDownloads")

        self.formLayout_2.setWidget(
            2, QFormLayout.ItemRole.LabelRole, self.cb_maxDownloads)

        self.le_lang_subtitles = QLineEdit(Config)
        self.le_lang_subtitles.setObjectName(u"le_lang_subtitles")
        self.le_lang_subtitles.setEnabled(False)

        self.formLayout_2.setWidget(
            12, QFormLayout.ItemRole.FieldRole, self.le_lang_subtitles)

        self.gridLayout_2.addLayout(self.formLayout_2, 3, 0, 2, 1)

        self.footer = QHBoxLayout()
        self.footer.setObjectName(u"footer")
        self.pb_save = QPushButton(Config)
        self.pb_save.setObjectName(u"pb_save")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.pb_save.setIcon(icon4)

        self.footer.addWidget(self.pb_save)

        self.pb_cancel = QPushButton(Config)
        self.pb_cancel.setObjectName(u"pb_cancel")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        self.pb_cancel.setIcon(icon5)

        self.footer.addWidget(self.pb_cancel)

        self.gridLayout_2.addLayout(self.footer, 8, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(8)
        self.cb_restrictFilename = QCheckBox(Config)
        self.cb_restrictFilename.setObjectName(u"cb_restrictFilename")

        self.gridLayout.addWidget(self.cb_restrictFilename, 1, 1, 1, 1)

        self.cb_noPlaylist = QCheckBox(Config)
        self.cb_noPlaylist.setObjectName(u"cb_noPlaylist")

        self.gridLayout.addWidget(self.cb_noPlaylist, 1, 2, 1, 1)

        self.cb_thumbnail = QCheckBox(Config)
        self.cb_thumbnail.setObjectName(u"cb_thumbnail")
        self.cb_thumbnail.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.cb_thumbnail, 0, 0, 1, 1)

        self.cb_embedSubs = QCheckBox(Config)
        self.cb_embedSubs.setObjectName(u"cb_embedSubs")

        self.gridLayout.addWidget(self.cb_embedSubs, 1, 0, 1, 1)

        self.cb_noOverwrites = QCheckBox(Config)
        self.cb_noOverwrites.setObjectName(u"cb_noOverwrites")

        self.gridLayout.addWidget(self.cb_noOverwrites, 0, 1, 1, 1)

        self.cb_metadata = QCheckBox(Config)
        self.cb_metadata.setObjectName(u"cb_metadata")

        self.gridLayout.addWidget(self.cb_metadata, 0, 2, 1, 1)

        self.cb_downloadArchive = QCheckBox(Config)
        self.cb_downloadArchive.setObjectName(u"cb_downloadArchive")

        self.gridLayout.addWidget(self.cb_downloadArchive, 2, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 6, 0, 1, 1)

        self.line_11 = QFrame(Config)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_11, 5, 0, 1, 1)

        self.line_13 = QFrame(Config)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.Shape.HLine)
        self.line_13.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_13, 7, 0, 1, 1)

        self.retranslateUi(Config)
        self.cb_cookies.clicked["bool"].connect(self.le_cookies.setEnabled)
        self.cb_limitRate.clicked["bool"].connect(self.le_limitRate.setEnabled)
        self.cb_proxy.clicked["bool"].connect(self.le_proxy.setEnabled)
        self.cb_maxDownloads.clicked["bool"].connect(
            self.sb_maxDownloads.setEnabled)
        self.cb_subtitles.clicked["bool"].connect(
            self.le_lang_subtitles.setEnabled)
        self.cb_cookies.clicked["bool"].connect(self.pb_cookies.setEnabled)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate(
            "Config", u"Configure", None))
        self.lb_filename.setText(
            QCoreApplication.translate("Config", u"Filename", None))
        self.lb_path.setText(
            QCoreApplication.translate("Config", u"Path", None))
        self.pb_revertFilename.setText("")
        self.pb_path.setText("")
        self.le_filename.setText(QCoreApplication.translate(
            "Config", u"%(title)s.%(ext)s", None))
        self.le_path.setPlaceholderText(
            QCoreApplication.translate("Config", u"select PATH", None))
        self.cb_cookies.setText(
            QCoreApplication.translate("Config", u"Cookies", None))
        self.le_cookies.setPlaceholderText(
            QCoreApplication.translate("Config", u"select FILE", None))
        self.pb_cookies.setText("")
        self.title.setText(QCoreApplication.translate(
            "Config", u"Adjust your Settings", None))
        self.lb_type.setText(
            QCoreApplication.translate("Config", u"Type", None))
        self.cb_type.setItemText(
            0, QCoreApplication.translate("Config", u"Video", None))
        self.cb_type.setItemText(
            1, QCoreApplication.translate("Config", u"Audio", None))

        self.lb_qvideo.setText(QCoreApplication.translate(
            "Config", u"Quality Video", None))
        self.cb_qvideo.setItemText(
            0, QCoreApplication.translate("Config", u"Best", None))
        self.cb_qvideo.setItemText(
            1, QCoreApplication.translate("Config", u"Worst", None))
        self.cb_qvideo.setItemText(
            2, QCoreApplication.translate("Config", u"360p", None))
        self.cb_qvideo.setItemText(
            3, QCoreApplication.translate("Config", u"480p", None))
        self.cb_qvideo.setItemText(
            4, QCoreApplication.translate("Config", u"720p", None))
        self.cb_qvideo.setItemText(
            5, QCoreApplication.translate("Config", u"1080p", None))
        self.cb_qvideo.setItemText(
            6, QCoreApplication.translate("Config", u"1440p", None))
        self.cb_qvideo.setItemText(
            7, QCoreApplication.translate("Config", u"2160p", None))

        self.lb_fvideo.setText(QCoreApplication.translate(
            "Config", u"Format Video", None))
        self.cb_fvideo.setItemText(
            0, QCoreApplication.translate("Config", u"mp4", None))
        self.cb_fvideo.setItemText(
            1, QCoreApplication.translate("Config", u"mkv", None))
        self.cb_fvideo.setItemText(
            2, QCoreApplication.translate("Config", u"mov", None))
        self.cb_fvideo.setItemText(
            3, QCoreApplication.translate("Config", u"webm", None))
        self.cb_fvideo.setItemText(
            4, QCoreApplication.translate("Config", u"avi", None))
        self.cb_fvideo.setItemText(
            5, QCoreApplication.translate("Config", u"flv", None))

        self.lb_qaudio.setText(QCoreApplication.translate(
            "Config", u"Quality Audio", None))
        self.cb_qaudio.setItemText(
            0, QCoreApplication.translate("Config", u"Best", None))
        self.cb_qaudio.setItemText(
            1, QCoreApplication.translate("Config", u"Worst", None))
        self.cb_qaudio.setItemText(
            2, QCoreApplication.translate("Config", u"64k", None))
        self.cb_qaudio.setItemText(
            3, QCoreApplication.translate("Config", u"96k", None))
        self.cb_qaudio.setItemText(
            4, QCoreApplication.translate("Config", u"128k", None))
        self.cb_qaudio.setItemText(
            5, QCoreApplication.translate("Config", u"192k", None))
        self.cb_qaudio.setItemText(
            6, QCoreApplication.translate("Config", u"256k", None))
        self.cb_qaudio.setItemText(
            7, QCoreApplication.translate("Config", u"320k", None))

        self.lb_faudio.setText(QCoreApplication.translate(
            "Config", u"Format Audio", None))
        self.cb_faudio.setItemText(
            0, QCoreApplication.translate("Config", u"aac", None))
        self.cb_faudio.setItemText(
            1, QCoreApplication.translate("Config", u"m4a", None))
        self.cb_faudio.setItemText(
            2, QCoreApplication.translate("Config", u"mp3", None))
        self.cb_faudio.setItemText(
            3, QCoreApplication.translate("Config", u"flac", None))
        self.cb_faudio.setItemText(
            4, QCoreApplication.translate("Config", u"ogg", None))
        self.cb_faudio.setItemText(
            5, QCoreApplication.translate("Config", u"opus", None))
        self.cb_faudio.setItemText(
            6, QCoreApplication.translate("Config", u"wav", None))
        self.cb_faudio.setItemText(
            7, QCoreApplication.translate("Config", u"webm", None))

        self.cb_subtitles.setText(
            QCoreApplication.translate("Config", u"Subtitles", None))
        self.cb_limitRate.setText(
            QCoreApplication.translate("Config", u"Limit Rate", None))
        self.le_limitRate.setText("")
        self.le_limitRate.setPlaceholderText(
            QCoreApplication.translate("Config", u"input RATE", None))
        self.cb_proxy.setText(
            QCoreApplication.translate("Config", u"Proxy", None))
        self.le_proxy.setPlaceholderText(
            QCoreApplication.translate("Config", u"input URL", None))
        self.cb_maxDownloads.setText(
            QCoreApplication.translate("Config", u"Max Downloads", None))
        self.le_lang_subtitles.setPlaceholderText(QCoreApplication.translate(
            "Config", u"enter the language abbreviation", None))
        self.pb_save.setText(
            QCoreApplication.translate("Config", u"Save", None))
        self.pb_cancel.setText(
            QCoreApplication.translate("Config", u"Cancel", None))
        self.cb_restrictFilename.setText(QCoreApplication.translate(
            "Config", u"Restrict Filename (ASCII)", None))
        self.cb_noPlaylist.setText(
            QCoreApplication.translate("Config", u"No Playlist", None))
        self.cb_thumbnail.setText(
            QCoreApplication.translate("Config", u"Thumbnail", None))
        self.cb_embedSubs.setText(QCoreApplication.translate(
            "Config", u"Embed Subtitles", None))
        self.cb_noOverwrites.setText(
            QCoreApplication.translate("Config", u"No Overwrites", None))
        self.cb_metadata.setText(
            QCoreApplication.translate("Config", u"Metadata", None))
        self.cb_downloadArchive.setText(
            QCoreApplication.translate("Config", u"Download Archive", None))
    # retranslateUi
