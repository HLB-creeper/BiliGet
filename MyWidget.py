from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QThread, Qt, QSize, QTimer
from PySide2.QtGui import QPainter, QPainterPath
from markdown import markdown

class ClickableLabel(QLabel):
    clicked: Signal = Signal()
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setScaledContents(True)

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()


class RoundClickableLabel(ClickableLabel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.is_round = True

    def paintEvent(self, event) -> None:
        if self.is_round:
            # 获取当前显示的图片
            pixmap = self.pixmap()
            if pixmap:
                radius = min(self.width(), self.height()) / 2
                # 创建 QPainter 对象
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
                # 绘制圆形剪裁区域
                path = QPainterPath()
                path.addRoundedRect(
                    0, 0, self.width(), self.height(), radius, radius)
                painter.setClipPath(path)
                # 绘制图片
                painter.drawPixmap(0, 0, pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            super().paintEvent(event)


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
        self.mousePressEvent = lambda event: None
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
        self.mousePressEvent = lambda event: None
        self.widget.mousePressEvent = lambda event: None
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)

class MarkdownViewer(QTextBrowser):
    def __init__(self, markdown_file):
        super().__init__()
        self.setReadOnly(True)
        self.setOpenExternalLinks(True)
        # 加载 Markdown 文件并显示内容
        self.load_markdown(markdown_file)

    def load_markdown(self, markdown_file):
        # 读取 Markdown 文件内容
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        # 将 Markdown 转换为 HTML
        html = markdown(markdown_text)
        # 设置 QTextBrowser 的内容为转换后的 HTML
        self.setHtml(html)
        # 根据 HTML 内容计算所需的大小
        QTimer.singleShot(0, self.adjust_size_to_content)

    def adjust_size_to_content(self):
        # 获取内容的字体和文档
        doc = self.document()
        doc_size = doc.size()  # 获取文档内容的大小
        print(doc_size)
        # 计算需要的宽度和高度
        width = doc_size.width() + 40  # 额外加些边距
        height = doc_size.height() + 40  # 额外加些边距
        # 设置 QTextBrowser 大小
        self.setMinimumSize(QSize(width, height))
        self.resize(width, height)  # 设置 QMainWindow 的大小