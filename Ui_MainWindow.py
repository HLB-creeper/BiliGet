# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QSize(750, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_title = QHBoxLayout()
        self.layout_title.setObjectName(u"layout_title")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 50))
        self.label.setMaximumSize(QSize(50, 50))

        self.layout_title.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 50))
        self.label_2.setMaximumSize(QSize(50, 50))

        self.layout_title.addWidget(self.label_2)

        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(18)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.layout_title.addWidget(self.label_title)


        self.verticalLayout.addLayout(self.layout_title)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_search = QWidget()
        self.tab_search.setObjectName(u"tab_search")
        self.verticalLayout_3 = QVBoxLayout(self.tab_search)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.combo_box_type = QComboBox(self.tab_search)
        self.combo_box_type.addItem("")
        self.combo_box_type.addItem("")
        self.combo_box_type.addItem("")
        self.combo_box_type.setObjectName(u"combo_box_type")

        self.horizontalLayout.addWidget(self.combo_box_type)

        self.line_edit_url = QLineEdit(self.tab_search)
        self.line_edit_url.setObjectName(u"line_edit_url")

        self.horizontalLayout.addWidget(self.line_edit_url)

        self.pbtn_search = QPushButton(self.tab_search)
        self.pbtn_search.setObjectName(u"pbtn_search")

        self.horizontalLayout.addWidget(self.pbtn_search)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.list_videos = QListWidget(self.tab_search)
        self.list_videos.setObjectName(u"list_videos")

        self.verticalLayout_3.addWidget(self.list_videos)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pbtn_select_all = QPushButton(self.tab_search)
        self.pbtn_select_all.setObjectName(u"pbtn_select_all")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbtn_select_all.sizePolicy().hasHeightForWidth())
        self.pbtn_select_all.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pbtn_select_all)

        self.pbtn_reverse = QPushButton(self.tab_search)
        self.pbtn_reverse.setObjectName(u"pbtn_reverse")
        sizePolicy.setHeightForWidth(self.pbtn_reverse.sizePolicy().hasHeightForWidth())
        self.pbtn_reverse.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pbtn_reverse)

        self.pbtn_download = QPushButton(self.tab_search)
        self.pbtn_download.setObjectName(u"pbtn_download")
        sizePolicy.setHeightForWidth(self.pbtn_download.sizePolicy().hasHeightForWidth())
        self.pbtn_download.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pbtn_download)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab_search, "")
        self.tab_download = QWidget()
        self.tab_download.setObjectName(u"tab_download")
        self.verticalLayout_2 = QVBoxLayout(self.tab_download)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.list_downloads = QListWidget(self.tab_download)
        self.list_downloads.setObjectName(u"list_downloads")

        self.verticalLayout_2.addWidget(self.list_downloads)

        self.tabWidget.addTab(self.tab_download, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"bilibili\u89c6\u9891\u4e0b\u8f7d\u5668", None))
        self.label.setText("")
        self.label_2.setText("")
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"bilibili\u89c6\u9891\u4e0b\u8f7d", None))
        self.combo_box_type.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5173\u952e\u8bcd", None))
        self.combo_box_type.setItemText(1, QCoreApplication.translate("MainWindow", u"\u94fe\u63a5", None))
        self.combo_box_type.setItemText(2, QCoreApplication.translate("MainWindow", u"BV\u53f7", None))

        self.pbtn_search.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.pbtn_select_all.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
        self.pbtn_reverse.setText(QCoreApplication.translate("MainWindow", u"\u53cd\u9009", None))
        self.pbtn_download.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_download), QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
    # retranslateUi

