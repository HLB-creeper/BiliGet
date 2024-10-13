# -*- coding:utf-8 -*-

from time import sleep, localtime, strftime
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, Qt, QThreadPool
from PySide2.QtGui import QPixmap
from Ui_MainWindow import Ui_MainWindow
from Ui_UserWindow import Ui_UserWindow
from MyWidget import *
from download import DownloadWorker
import login, video


class MainWindow(QMainWindow, Ui_MainWindow):
    add_video: Signal = Signal(QPixmap, str, str, str, str)
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self._setup_ui()

        # 类型批注及初始化
        self.layout_title: QHBoxLayout
        self.combo_box_type: QComboBox
        self.line_edit_url: QLineEdit
        self.pbtn_search: QPushButton
        self.list_videos: QListWidget
        self.list_downloads: QListWidget
        self.tabWidget: QTabWidget
        # self.list_downloads.setSelectionMode(QListWidget.NoSelection)
        # self.list_videos.setSelectionMode(QListWidget.NoSelection)
        style_list = """
QListWidget::item {
    margin:10px;
    border:3px solid #ccc;
    border-radius:10px;
    background-color:#f5f5f5;
    color:#333;
} 
QScrollBar{
    border: 3px solid #ccc;
    border-radius: 5px;
    padding: 1px;
    height: 20px;
    width: 20px;
}
QScrollBar::handle{
    border-radius: 3px;
    background: #aaaaaa;
    min-width: 16px;
    min-height: 16px;
}
QScrollBar::handle:hover{
    background: #8c8c8c;
}
QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar::add-page, QScrollBar::sub-page {
    width: 0px;
    background: transparent;
}
QScrollArea{
    border: none;
}
"""
        self.tabWidget.setCurrentIndex(0)
        self.list_videos.setStyleSheet(style_list)
        self.list_downloads.setStyleSheet(style_list)
        # self.list_videos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) # 总是显示滚动条
        self.pbtn_download: QPushButton
        self.cookie: dict = {
            "DedeUserID": "3494353660020892", 
            "DedeUserID__ckMd5": "47b872492f6c0cc3", 
            "SESSDATA": "943378c1%2C1740575427%2C3e5d9%2A81CjBfgl8PkPGvEPG-lPgr-LtPUVC3mdeEcHjgwwl1wjLByGJFopL6Bh9zOdoI8mf9eD8SVl82OFp1MzJ1M0JmTzlKSHpTcnphZVhUVmVUSjNEQ1Y1TjQ4d2NYZFNUWXRhdmpUQU10RjNKbUFrZlBxTTRLaEJsU0tkUjVQOHVtYUtCeklsWUtpcHlBIIEC", 
            "bili_jct": "574a4913903f83540e07122e3d237d63", 
            "sid": "8k9ddh79"
        }
        self.set_cookie(self.cookie)
        # self.cookie: dict = {}
        self.search_thread: MyThread = None
        self.pbtn_reverse: QPushButton
        self.pbtn_select_all: QPushButton
        self.thread_pool = QThreadPool.globalInstance()
        max_threads = min(50, self.thread_pool.maxThreadCount())
        self.thread_pool.setMaxThreadCount(max_threads)  # 设置最大线程数
        # self.workers: list[DownloadWorker] = []

        # 绑定信号与槽
        self.user_window.send_cookie.connect(self.set_cookie)
        self.user_window.clear_cookie.connect(self.clear_cookie)
        self.btn_user.clicked.connect(self.login)
        self.btn_setting.clicked.connect(lambda: print("setting clicked"))
        self.pbtn_search.clicked.connect(self.search_video)
        self.add_video.connect(self.add_video_item)
        self.pbtn_download.clicked.connect(self.start_download)
        # self.list_videos.itemClicked.connect(lambda item: print(item.nameLabel.text(), end=''))
        self.pbtn_select_all.clicked.connect(self.select_all)
        self.pbtn_reverse.clicked.connect(self.select_reverse)

    def _setup_ui(self) -> None:
        self.setupUi(self)
        
        # 登录窗口
        self.user_window = UserWindow()
        self.user_window.mode = 'logout'

        # 用户按钮
        self.btn_user: ClickableLabel = ClickableLabel()
        self.btn_user.setFixedSize(50, 50)
        self.btn_user.setPixmap(QPixmap('./img/user.png'))
        self.layout_title.addWidget(self.btn_user)

        # 设置按钮
        self.btn_setting: ClickableLabel = ClickableLabel()
        self.btn_setting.setFixedSize(50, 50)
        self.btn_setting.setPixmap(QPixmap('./img/setting.png'))
        self.layout_title.addWidget(self.btn_setting)

    # ====================槽函数====================
    def login(self) -> None:
        if self.user_window.isVisible():
            QMessageBox.warning(self, '警告', '请先关闭登录窗口！')
            return
        if not self.cookie:
            self.user_window.mode = 'login'
            self.user_window.show()
        else:
            self.user_window.mode = 'logout'
            self.user_window.show()
    
    def closeEvent(self, event) -> None:
        self.user_window.close()
        try:
            self.search_thread.terminate()
        except Exception as e:
            # print(e)
            pass
        event.accept()

    def set_cookie(self, cookie: dict) -> None:
        self.cookie = cookie
        login.session.cookies.update(cookie)
        video.headers["Cookie"] = '; '.join([f'{key}={value}' for key, value in cookie.items()])
        print("get cookie:", video.headers["Cookie"])

    def clear_cookie(self) -> None:
        self.cookie = {}
        video.headers["cookie"] = ""
        print(f"clear cookie: {self.cookie}")

    def search_video(self) -> None:
        self.list_videos.clear()
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.terminate()
        get_type: int = self.combo_box_type.currentIndex() # 0: 关键词, 1: 链接
        get_text: str = self.line_edit_url.text()
        if not get_text:
            QMessageBox.warning(self, '警告', '请输入搜索内容！')
            return
        if get_type == 0:
            self.search_thread = MyThread(parent=self, func=lambda: self.get_search_result(keyword=get_text))
            self.search_thread.start()
        if get_type == 1:
            pass
    
    def add_video_item(self, img: QPixmap, title: str, author: str, pubdate: int, bvid: str) -> None:
        VideoItem(img, title, author, pubdate, bvid, self.list_videos)

    def start_download(self) -> None:
        items: list[VideoItem] = [self.list_videos.item(i) for i in range(self.list_videos.count())]
        num: int = 0
        if not items:
            QMessageBox.warning(self, '警告', '没有选中任何视频')
            return
        for item in items:
            if item.check_box.isChecked():
                num += 1
                if num >= 50:
                    QMessageBox.warning(self, '警告', '一次最多只能下载50个视频')
                    return
                # print(f"start download: {item.bvid}")
                download_item = DownloadItem(item.img, item.title, item.author, item.bvid, self.list_downloads)
                worker = DownloadWorker(item.bvid)
                worker.signals.progress.connect(download_item.progress.setValue)
                worker.signals.finished.connect(lambda: self.download_finished(download_item))
                worker.signals.paused.connect(lambda: print("下载已暂停"))
                worker.signals.resumed.connect(lambda: print("下载已恢复"))
                # self.workers.append(worker)
                self.thread_pool.start(worker)
                self.list_videos.takeItem(self.list_videos.row(item))

    def select_all(self) -> None:
        for i in range(self.list_videos.count()):
            item = self.list_videos.item(i)
            item.check_box.setChecked(True)
    
    def select_reverse(self) -> None:
        for i in range(self.list_videos.count()):
            item = self.list_videos.item(i)
            item.check_box.toggle()

    # ====================自定义函数====================
    def get_search_result(self, keyword: str) -> None:
        data = video.get_response(f"https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&page=1&page_size=50&platform=pc&keyword={keyword}").json()

        for i in range(50):
            bvid = data["data"]["result"][i]["bvid"]
            title = data["data"]["result"][i]["title"].replace('<em class="keyword">', '').replace('</em>', '')
            author = data["data"]["result"][i]["author"]
            img_url = data["data"]["result"][i]["pic"]
            pubdate = data["data"]["result"][i]["pubdate"]
            pubdate = self.trans_data(pubdate)
            if not (img_url and title and author and bvid):
                continue
            img_url = "https:" + img_url if img_url[0:2]=="//" else img_url
            img_format: str = img_url.split(".")[-1]
            img_bytes: bytes = video.get_response(img_url).content
            img = QPixmap()
            img.loadFromData(img_bytes, img_format)
            # print(f"get video info: {title}, {author}, {bvid}, {img_url}, {pubdate}")
            self.add_video.emit(img, title, author, pubdate, bvid)

    def trans_data(self, timeStamp):
        # print(f"trans data: {timeStamp}")
        timeArray = localtime(timeStamp)
        otherStyleTime = strftime("%Y年%m月%d日 %H:%M", timeArray)
        # print(f"other style time: {otherStyleTime}")
        return otherStyleTime

    def download_finished(self, item: DownloadItem) -> None:
        self.list_downloads.takeItem(self.list_downloads.row(item))
        # self.workers.remove(self.workers.index(item))

    # def get_video_type(self, bvid: str) -> None:
    # 	# data = video.get_response(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}").json()
    # 	pass

    # ====================重写事件====================
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.search_video()

class UserWindow(QMainWindow, Ui_UserWindow):
    send_cookie: Signal = Signal(dict)
    clear_cookie: Signal = Signal()
    def __init__(self, parent=None, mode: str = 'login') -> None:
        super(UserWindow, self).__init__(parent)
        self._setup_ui()

        # 类型批注及初始化
        self.label: QLabel
        self.mode: str = mode
        self.layout_qrcode: QVBoxLayout
        self.cookie: dict = {}
        self.status: int = 0 # 0: 等待, 1: 已登录, 2: 重试
        self.check_login_thread: MyThread = MyThread(parent=self, func=self.check_login)
        self.is_ok: bool = False
        self.name: str = ""
        self.face: QPixmap = None
        self.user_info: dict = {}

        # 绑定信号与槽
        self.image.clicked.connect(self.on_image_clicked)

    def _setup_ui(self) -> None:
        self.setupUi(self)

        # 二维码
        self.image: ClickableLabel = ClickableLabel()
        self.image.setFixedSize(400, 400)
        self.layout_qrcode.addWidget(self.image)

    def login(self) -> None:
        self.status = 0
        self.mode = "login"
        self.is_ok = False
        print('login mode')
        qrcode = login.get_qrcode()
        self.image.setPixmap(qrcode)
        self.label.setText('请使用bilibili客户端扫描二维码登录')
        # print(self.check_login_thread)
        self.check_login_thread.start()

    def closeEvent(self, event) -> None:
        try:
            if self.check_login_thread.isRunning():
                # self.check_login_thread.terminate()
                self.is_ok = True
                self.check_login_thread.wait()
                print('stop check login status thread')
        except:
            pass
        event.accept()
    
    def showEvent(self, event) -> None:
        print('show user window')
        if self.mode == "login":
            self.login()
            event.accept()
            return
        if self.mode == "logout":
            self.status = 1
            self.is_ok = True
            if not (self.user_info):
                self.user_info = login.get_user_info()
                print(f"get user info: {self.user_info}")
            self.image.setPixmap(self.user_info["image"])
            self.label.setText(f'欢迎, {self.user_info["name"]}')

    def check_login(self) -> None:
        while not self.is_ok:
            status = login.get_status()
            if status == 0: # 已确认登录
                self.status = 1
                self.is_ok = True
                self.cookie = login.session.cookies.get_policy()
                self.send_cookie.emit(self.cookie)
                self.user_info = login.get_user_info()
                print(f"get user info: {self.user_info}")
                self.image.setPixmap(self.user_info["image"])
                self.label.setText(f'欢迎, {self.user_info["name"]}')
                print(f"login success")
            elif status == 86101: # 未扫码
                pass
            elif status == 86090: # 二维码已扫码未确认
                self.image.setPixmap(QPixmap('./img/ok.png'))
                self.label.setText('已扫描二维码, 请确认登录')
            elif status == 86038: # 二维码已失效
                self.image.setPixmap(QPixmap('./img/refresh.png'))
                self.status = 2
                self.is_ok = True
                print('qrcode expired')
                self.label.setText('二维码已失效, 请刷新')
            print(f"check login status: {status}")
            sleep(1)

    def on_image_clicked(self) -> None:
        if self.status == 2:
            self.login()
        if self.status == 1:
            if QMessageBox.question(
                self, 
                '确认', 
                '确认退出登录吗？', 
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            ) == QMessageBox.Yes:
                self.clear_cookie.emit()
                self.login()

def main() -> None:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()