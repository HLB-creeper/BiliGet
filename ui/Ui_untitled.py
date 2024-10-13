# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_widget(object):
    def setupUi(self, widget):
        if not widget.objectName():
            widget.setObjectName(u"widget")
        widget.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image_lable = QLabel(widget)
        self.image_lable.setObjectName(u"image_lable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_lable.sizePolicy().hasHeightForWidth())
        self.image_lable.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.image_lable)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_lable = QLabel(widget)
        self.title_lable.setObjectName(u"title_lable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.title_lable.sizePolicy().hasHeightForWidth())
        self.title_lable.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.title_lable)

        self.progress = QProgressBar(widget)
        self.progress.setObjectName(u"progress")

        self.verticalLayout.addWidget(self.progress)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(widget)

        QMetaObject.connectSlotsByName(widget)
    # setupUi

    def retranslateUi(self, widget):
        widget.setWindowTitle(QCoreApplication.translate("widget", u"Form", None))
        self.image_lable.setText("")
        self.title_lable.setText("")
    # retranslateUi

