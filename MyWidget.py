from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QThread, Qt, QSize
from PySide2.QtGui import QPixmap
import sys

class ClickableLabel(QLabel):
    clicked: Signal = Signal()
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setScaledContents(True)

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()


class MyThread(QThread):
    def __init__(self, func, parent=None) -> None:
        super().__init__(parent)
        self.func = func

    def run(self) -> None:
        self.func()


class VideoItem(QListWidgetItem):
    def __init__(self, img, title, author, pubdate, bvid, parent: QListWidget):
        super().__init__(parent)
        self.img = img
        self.title = title
        self.author = author
        self.pubdate = pubdate
        self.bvid = bvid
        self.widget = QWidget()
        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setText(f"<b><big>{title}</big></b><br>{author} · {pubdate}")
        # print(pubdate)
        self.avatorLabel = QLabel()
        self.avatorLabel.setPixmap(img.scaled(QSize(250, 250), Qt.KeepAspectRatio))
        self.check_box = QCheckBox()
        self.check_box.setText("")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.avatorLabel)
        self.hbox.addWidget(self.nameLabel)
        self.hbox.addWidget(self.check_box)
        self.widget.setLayout(self.hbox)
        self.widget.mousePressEvent = lambda event: self.check_box.toggle()
        self.setSizeHint(self.widget.sizeHint())
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)


class DownloadItem(QListWidgetItem):
    def __init__(self, img, title, author, bvid, parent: QListWidget):
        super().__init__(parent)
        style = """
QProgressBar {
    background-color: #b3d9f7;
    border-radius: 5px;
    text-align: center;
    font-family: Consolas, 'Courier New', monospace;
    border: 2px solid #4ea2e2;
}
QProgressBar::chunk {
    background-color: #4ea2e2;
    border-radius: 5px;
    margin: 3px;
}
"""
        self.bvid = bvid
        self.img = img
        self.title = title
        self.author = author
        self.widget = QWidget()
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.image_lable = QLabel(self.widget)
        self.image_lable.setPixmap(img.scaled(QSize(250, 250), Qt.KeepAspectRatio))
        self.horizontalLayout.addWidget(self.image_lable)
        self.verticalLayout = QVBoxLayout()
        self.title_lable = QLabel(self.widget)
        self.title_lable.setWordWrap(True)
        self.title_lable.setText(f"<b><big>{title}</big></b><br>{author}")
        self.title_lable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.title_lable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.title_lable)
        self.progress = QProgressBar(self.widget)
        self.progress.setStyleSheet(style)
        self.progress.setValue(0)
        self.verticalLayout.addWidget(self.progress)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setSizeHint(self.widget.sizeHint())
        # self.widget.mousePressEvent = lambda event: print('', end='')
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)