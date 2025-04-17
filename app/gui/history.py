# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'historyFNLlyS.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
                               QLabel, QPushButton, QSizePolicy, QTextEdit,
                               QWidget)


class Ui_History(object):
    def setupUi(self, History):
        if not History.objectName():
            History.setObjectName(u"History")
        History.resize(480, 640)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        History.setWindowIcon(icon)
        History.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.gridLayout = QGridLayout(History)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(History)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.textEdit = QTextEdit(History)
        self.textEdit.setObjectName(u"textEdit")
        font1 = QFont()
        font1.setPointSize(10)
        self.textEdit.setFont(font1)
        self.textEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)

        self.widget = QWidget(History)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnSaveHistory = QPushButton(self.widget)
        self.btnSaveHistory.setObjectName(u"btnSaveHistory")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.btnSaveHistory.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.btnSaveHistory)

        self.btnDeleteHistory = QPushButton(self.widget)
        self.btnDeleteHistory.setObjectName(u"btnDeleteHistory")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.btnDeleteHistory.setFont(font2)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.btnDeleteHistory.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btnDeleteHistory)

        self.gridLayout.addWidget(self.widget, 2, 0, 1, 1)

        self.retranslateUi(History)

        QMetaObject.connectSlotsByName(History)
    # setupUi

    def retranslateUi(self, History):
        History.setWindowTitle(
            QCoreApplication.translate("History", u"History", None))
        self.label.setText(QCoreApplication.translate(
            "History", u"Download History", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate(
            "History", u"Here you will see a list of all downloaded items.", None))
        self.btnSaveHistory.setText(
            QCoreApplication.translate("History", u"Generate", None))
        self.btnDeleteHistory.setText(
            QCoreApplication.translate("History", u"Delete", None))
    # retranslateUi
