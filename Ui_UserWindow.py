# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UserWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UserWindow(object):
    def setupUi(self, UserWindow):
        if not UserWindow.objectName():
            UserWindow.setObjectName(u"UserWindow")
        UserWindow.resize(410, 450)
        UserWindow.setMinimumSize(QSize(410, 450))
        self.ugqids = QWidget(UserWindow)
        self.ugqids.setObjectName(u"ugqids")
        self.verticalLayout = QVBoxLayout(self.ugqids)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_qrcode = QVBoxLayout()
        self.layout_qrcode.setObjectName(u"layout_qrcode")
        self.label = QLabel(self.ugqids)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.layout_qrcode.addWidget(self.label)


        self.verticalLayout.addLayout(self.layout_qrcode)

        UserWindow.setCentralWidget(self.ugqids)

        self.retranslateUi(UserWindow)

        QMetaObject.connectSlotsByName(UserWindow)
    # setupUi

    def retranslateUi(self, UserWindow):
        UserWindow.setWindowTitle(QCoreApplication.translate("UserWindow", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("UserWindow", u"\u8bf7\u4f7f\u7528bilibili\u5ba2\u6237\u7aef\u626b\u63cf\u4e8c\u7ef4\u7801\u767b\u5f55", None))
    # retranslateUi

