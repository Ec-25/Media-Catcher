# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'mainbJDvFz.ui'
##
# Created by: Qt User Interface Compiler version 6.9.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
                               QLineEdit, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QSpacerItem, QTableView,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 640)
        MainWindow.setMinimumSize(QSize(480, 640))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkWired))
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setMenuRole(QAction.MenuRole.AboutRole)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionConfiguration = QAction(MainWindow)
        self.actionConfiguration.setObjectName(u"actionConfiguration")
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionEnglish.setCheckable(True)
        self.actionEnglish.setChecked(True)
        self.actionSpanish = QAction(MainWindow)
        self.actionSpanish.setObjectName(u"actionSpanish")
        self.actionSpanish.setCheckable(True)
        self.actionClear_List = QAction(MainWindow)
        self.actionClear_List.setObjectName(u"actionClear_List")
        self.actionHistory = QAction(MainWindow)
        self.actionHistory.setObjectName(u"actionHistory")
        self.actionDebug = QAction(MainWindow)
        self.actionDebug.setObjectName(u"actionDebug")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 2)

        self.tableMediaContent = QTableView(self.centralwidget)
        self.tableMediaContent.setObjectName(u"tableMediaContent")
        font = QFont()
        font.setPointSize(12)
        self.tableMediaContent.setFont(font)
        self.tableMediaContent.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableMediaContent.setTabKeyNavigation(False)
        self.tableMediaContent.setDragDropOverwriteMode(False)
        self.tableMediaContent.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.tableMediaContent.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.tableMediaContent, 2, 0, 1, 2)

        self.inputUrl = QLineEdit(self.centralwidget)
        self.inputUrl.setObjectName(u"inputUrl")
        self.inputUrl.setFont(font)
        self.inputUrl.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.inputUrl, 0, 0, 1, 1)

        self.btnAddUrl = QPushButton(self.centralwidget)
        self.btnAddUrl.setObjectName(u"btnAddUrl")
        self.btnAddUrl.setFont(font)

        self.gridLayout_2.addWidget(self.btnAddUrl, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 480, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuLanguage = QMenu(self.menuEdit)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionHistory)
        self.menuEdit.addAction(self.actionConfiguration)
        self.menuEdit.addAction(self.menuLanguage.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionClear_List)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionSpanish)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDebug)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Media Catcher", None))
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(
            QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionConfiguration.setText(
            QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.actionEnglish.setText(
            QCoreApplication.translate("MainWindow", u"English", None))
        self.actionSpanish.setText(QCoreApplication.translate(
            "MainWindow", u"Espa\u00f1ol", None))
        self.actionClear_List.setText(
            QCoreApplication.translate("MainWindow", u"Clear List", None))
        self.actionHistory.setText(
            QCoreApplication.translate("MainWindow", u"History", None))
        self.actionDebug.setText(
            QCoreApplication.translate("MainWindow", u"Debug", None))
        self.inputUrl.setPlaceholderText(QCoreApplication.translate(
            "MainWindow", u"URL of the multimedia content", None))
        self.btnAddUrl.setText(
            QCoreApplication.translate("MainWindow", u"Add", None))
        self.menuFile.setTitle(
            QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(
            QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuLanguage.setTitle(
            QCoreApplication.translate("MainWindow", u"Language", None))
        self.menuHelp.setTitle(
            QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi
