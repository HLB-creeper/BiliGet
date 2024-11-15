# -*- coding:utf-8 -*-

import json
from re import match
from math import ceil
from time import sleep, localtime, strftime
# from typing import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, Qt, QThreadPool
from PySide2.QtGui import QPixmap, QFont
from Ui_MainWindow import Ui_MainWindow
# from Ui_UserWindow import Ui_UserWindow
from MyWidget import *
from download import DownloadWorker
import func
import login


class MainWindow(QMainWindow, Ui_MainWindow):
    add_video: Signal = Signal(QPixmap, str, str, str, str)
    show_warning: Signal = Signal(str)
    send_cookie: Signal = Signal(dict)
    clear_cookie: Signal = Signal()
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self._setup_ui()

        # 类型批注及初始化
        self.rb_search: QRadioButton
        self.rb_download: QRadioButton
        self.rb_settings: QRadioButton
        self.list_settings: QListWidget
        self.layout_title: QHBoxLayout
        self.combo_box_type: QComboBox
        self.line_edit_url: QLineEdit
        self.pbtn_search: QPushButton
        self.list_videos: QListWidget
        self.list_downloads: QListWidget
        self.stackedWidget: QStackedWidget
        self.login_status: int = 0 # 0: 未登录且未生成二维码, 1: 已登录, 2: 等待, 3: 重试
        self.check_login_thread: MyThread = MyThread(parent=self, func=self.check_login)
        # self.list_downloads.setSelectionMode(QListWidget.NoSelection)
        # self.list_videos.setSelectionMode(QListWidget.NoSelection)
        with open('style.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        self.stackedWidget.setCurrentIndex(0)
        # self.list_videos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) # 总是显示滚动条
        self.pbtn_download: QPushButton
        self.cookie: str = ""
        self.user_info: dict = {}
        self.is_ok: bool = False
        self.search_thread: MyThread = None
        self.pbtn_reverse: QPushButton
        self.pbtn_select_all: QPushButton
        self.thread_pool = QThreadPool.globalInstance()
        max_threads = min(50, self.thread_pool.maxThreadCount())
        self.thread_pool.setMaxThreadCount(max_threads)  # 设置最大线程数
        # self.workers: list[DownloadWorker] = []
        self.read_config()

        # 绑定信号与槽
        self.rb_search.clicked.connect(lambda: self.change_tab(0))
        self.rb_download.clicked.connect(lambda: self.change_tab(1))
        self.rb_settings.clicked.connect(lambda: self.change_tab(2))
        # self.user_window.send_cookie.connect(self.update_cookie)
        # self.user_window.clear_cookie.connect(lambda: self.update_cookie(""))
        # self.user_window.write_config.connect(self.write_config)
        self.btn_user.clicked.connect(self.on_user_clicked)
        # self.btn_setting.clicked.connect(lambda: print("setting clicked"))
        self.pbtn_search.clicked.connect(self.search_video)
        self.add_video.connect(self.add_video_item)
        self.pbtn_download.clicked.connect(self.start_download)
        # self.list_videos.itemClicked.connect(lambda item: print(item.nameLabel.text(), end=''))
        self.pbtn_select_all.clicked.connect(self.select_all)
        self.pbtn_reverse.clicked.connect(self.select_reverse)
        self.show_warning.connect(lambda msg: QMessageBox.warning(self, '警告', msg))

    def _setup_ui(self) -> None:
        self.setupUi(self)
        # 设置界面初始化
        # -----用户设置-----
        user_widget = QWidget()
        layout = QHBoxLayout(user_widget)
        self.btn_user: RoundClickableLabel = RoundClickableLabel()
        self.btn_user.setFixedSize(150, 150)
        # self.btn_user.setPixmap(QPixmap('./img/user.png'))
        layout.addWidget(self.btn_user)
        self.label_user = QLabel()
        self.label_user.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        layout.addWidget(self.label_user)
        user_item = QListWidgetItem(self.list_settings)
        user_item.setSizeHint(QSize(self.list_settings.width(), 220))
        self.list_settings.addItem(user_item)
        self.list_settings.setItemWidget(user_item, user_widget)
        # -----使用说明-----
        markdown_widget = MarkdownViewer("./README.md")
        markdown_item = QListWidgetItem(self.list_settings)
        markdown_item.setSizeHint(QSize(self.list_settings.width(), markdown_widget.height()+50))
        self.list_settings.addItem(markdown_item)
        self.list_settings.setItemWidget(markdown_item, markdown_widget)

    # ====================槽函数====================
    def change_tab(self, index: int) -> None:
        now_index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(index)
        if now_index == 2:
            try:
                self.check_login_thread.terminate()
                print('stop check login status thread')
            except:
                pass
        if index == 2:
            if self.login_status == 1:
                self.is_ok = True
                if not (self.user_info):
                    self.user_info = login.get_user_info()
                    print(f"get user info: {self.user_info}")
                self.btn_user.is_round = True
                self.btn_user.setPixmap(self.user_info["image"])
                self.label_user.setText(f'欢迎, {self.user_info["name"]}')
            else:
                self.login()
                return

    def login(self) -> None:
        self.login_status = 0
        self.mode = "login"
        self.is_ok = False
        print('login mode')
        qrcode = login.get_qrcode()
        self.btn_user.setPixmap(qrcode)
        self.btn_user.is_round = False
        self.label_user.setText('请使用bilibili客户端扫描二维码登录')
        # print(self.check_login_thread)
        self.check_login_thread.start()

    def update_cookie(self, cookies: str = None) -> None:
        self.write_config()
        if(cookies != None): 
            self.cookie = cookies
        if self.cookie: 
            self.login_status = 1
        login.session.headers.update({"Cookie": self.cookie})
        func.headers["Cookie"] = self.cookie
        # self.update_uface()
        self.write_config()

    def search_video(self) -> None:
        get_type: int = self.combo_box_type.currentIndex() # 0: 关键词, 1: 链接
        get_text: str = self.line_edit_url.text()
        if not get_text:
            QMessageBox.warning(self, '警告', '请输入搜索内容！')
            return
        if not self.cookie:
            QMessageBox.warning(self, '警告', '请先登录！')
            return
        self.list_videos.clear()
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.terminate()
        self.search_thread = MyThread(parent=self, func=lambda: self.get_search_result(keyword=get_text, get_type=get_type))
        self.search_thread.start()
    
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
    
    def on_user_clicked(self) -> None:
        if self.login_status == 1:
            if QMessageBox.question(
                self, 
                '确认', 
                '确认退出登录吗？', 
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            ) == QMessageBox.Yes:
                self.clear_cookie.emit()
            else:
                return
        self.login()
    
    def select_reverse(self) -> None:
        for i in range(self.list_videos.count()):
            item = self.list_videos.item(i)
            item.check_box.toggle()

    # ====================自定义函数====================
    def get_search_result(self, keyword: str, get_type: int) -> None:
        if get_type == 0: # 关键词搜索
            data = func.get_response(url=f"https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&page=1&page_size=50&platform=pc&keyword={keyword}").json()
            for i in range(50):
                info = self.get_search_info(data["data"]["result"][i])
                author = data["data"]["result"][i]["author"]
                if not (info and author):
                    continue
                self.add_video.emit(info["img"], info["title"], author, info["pubdate"], data["data"]["result"][i]["bvid"])
        if get_type == 1: # 链接搜索
            if(match(r"^https://www\.bilibili\.com/video/BV[a-zA-Z0-9]+.*", keyword) is not None):
                bv = match(r"^https://www\.bilibili\.com/video/(BV[a-zA-Z0-9]+).*", keyword).group(1)
                print(bv)
                data = func.get_response(url=f"https://api.bilibili.com/x/web-interface/view?bvid={bv}").json()
                if(data["code"]!=0):
                    self.show_warning.emit('链接错误：bv号不存在！')
                    return
                info = self.get_search_info(data["data"])
                author = data["data"]["owner"]["name"]
                if not (info and author):
                    return
                self.add_video.emit(info["img"], info["title"], author, info["pubdate"], bv)
            elif match(r"^https://space\.bilibili\.com/\d+/channel/collectiondetail\?sid=(\d+).*", keyword) is not None:
                mid, sid = match(r"^https://space\.bilibili\.com/(\d+)/channel/collectiondetail\?sid=(\d+).*", keyword).groups()
                # https://api.bilibili.com/x/polymer/web-space/seasons_archives_list?mid={mid}&season_id={sid}&page_size=100&page_num=1
                data = func.get_response(url=f"https://api.bilibili.com/x/polymer/web-space/seasons_archives_list?mid={mid}&season_id={sid}&page_size=1&page_num=1").json()
                total = data["data"]["meta"]["total"]
                name = data["data"]["meta"]["name"]
                for page in range(ceil(total/100)):
                    data = func.get_response(url=f"https://api.bilibili.com/x/polymer/web-space/seasons_archives_list?mid={mid}&season_id={sid}&page_size=100&page_num={page+1}").json()
                    for i in range(len(data["data"]["aids"])):
                        info = self.get_search_info(data["data"]["archives"][i], use_ctime=True)
                        if not (info and name):
                            continue
                        self.add_video.emit(info["img"], info["title"], name, info["pubdate"], data["data"]["archives"][i]["bvid"])
        if get_type == 2: # BV号
            # print("BV号搜索", keyword)
            data = func.get_response(url=f"https://api.bilibili.com/x/web-interface/view?bvid={keyword}").json()
            if(data["code"]!=0):
                self.show_warning.emit('输入错误，请输入正确的BV号！')
                return
            info = self.get_search_info(data["data"])
            author = data["data"]["owner"]["name"]
            if not (info and author):
                return
            self.add_video.emit(info["img"], info["title"], author, info["pubdate"], keyword)
    
    def get_search_info(self, data, use_ctime: bool = False) -> dict:
        bvid = data["bvid"]
        title = data["title"].replace('<em class="keyword">', '').replace('</em>', '')
        img_url = data["pic"]
        if use_ctime:
            pubdate = data["ctime"]
        else:
            pubdate = data["pubdate"]
        pubdate = self.trans_data(pubdate)
        if not (img_url and title and bvid):
            return {}
        img_url = "https:" + img_url if img_url[0:2]=="//" else img_url
        img_format: str = img_url.split(".")[-1]
        img_bytes: bytes = func.get_response(img_url).content
        img = QPixmap()
        img.loadFromData(img_bytes, img_format)
        return {
            "img" : img,
            "title" : title,
            "pubdate" : pubdate
        }

    def trans_data(self, timeStamp):
        # print(f"trans data: {timeStamp}")
        timeArray = localtime(timeStamp)
        otherStyleTime = strftime("%Y{y}%m{m}%d{d} %H:%M", timeArray).format(y='年', m='月', d='日')
        # print(f"other style time: {otherStyleTime}")
        return otherStyleTime

    def download_finished(self, item: DownloadItem) -> None:
        self.list_downloads.takeItem(self.list_downloads.row(item))
        # self.workers.remove(self.workers.index(item))

    def read_config(self) -> None:
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.__dict__.update(config)
                self.update_cookie(config['cookie'])
                print("read config:", config)
        except Exception as e:
            QMessageBox.warning(self, '警告', '读取配置文件(config.json)错误，已重新创建配置文件')
            print("read config error: ", e)
            self.write_config()

    def write_config(self) -> None:
        config = {
            'cookie': self.cookie
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print("write config:", config)
    
    def update_uface(self) -> None:
        if not self.cookie:
            return
        if not (self.user_info):
            self.user_info = login.get_user_info()
            print(f"get user info: {self.user_info}")
        self.btn_user.is_round = True
        self.btn_user.setPixmap(self.user_info["image"])
    
    def check_login(self) -> None:
        while not self.is_ok:
            status = login.get_status()
            if status == 0: # 已确认登录
                self.login_status = 1
                self.is_ok = True
                self.cookie = '; '.join([f'{key}={value}' for key, value in login.session.cookies.get_dict().items()])
                self.send_cookie.emit(self.cookie)
                self.write_config()
                self.user_info = login.get_user_info()
                print(f"get user info: {self.user_info}")
                self.btn_user.is_round = True
                self.btn_user.setPixmap(self.user_info["image"])
                self.label_user.setText(f'欢迎, {self.user_info["name"]}')
                print(f"login success")
            elif status == 86101: # 未扫码
                self.login_status = 2
            elif status == 86090: # 二维码已扫码未确认
                self.btn_user.is_round = True
                self.btn_user.setPixmap(QPixmap('./img/ok.png'))
                self.label_user.setText('已扫描二维码, 请确认登录')
                self.login_status = 2
            elif status == 86038: # 二维码已失效
                self.btn_user.is_round = True
                self.btn_user.setPixmap(QPixmap('./img/refresh.png'))
                self.login_status = 3
                self.is_ok = True
                print('qrcode expired')
                self.label_user.setText('二维码已失效, 请刷新')
            print(f"check login status: {status}")
            sleep(1)

    # ====================重写事件====================
    def closeEvent(self, event) -> None:
        # self.user_window.close()
        try:
            self.search_thread.terminate()
        except Exception as e:
            # print(e)
            pass
        try:
            self.check_login_thread.terminate()
        except Exception as e:
            # print(e)
            pass
        event.accept()
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.search_video()

# class UserWindow(QMainWindow, Ui_UserWindow):
#     send_cookie: Signal = Signal(dict)
#     clear_cookie: Signal = Signal()
#     write_config: Signal = Signal()
#     def __init__(self, parent=None, mode: str = 'login') -> None:
#         super(UserWindow, self).__init__(parent)
#         self._setup_ui()

#         # 类型批注及初始化
#         self.label: QLabel
#         self.mode: str = mode
#         self.layout_qrcode: QVBoxLayout
#         self.cookie: str = ""
#         self.login_status: int = 0 # 0: 等待, 1: 已登录, 2: 重试
#         self.check_login_thread: MyThread = MyThread(parent=self, func=self.check_login)
#         self.is_ok: bool = False
#         self.name: str = ""
#         self.face: QPixmap = None
#         self.user_info: dict = {}

#         # 绑定信号与槽
#         self.image.clicked.connect(self.on_image_clicked)

#     def _setup_ui(self) -> None:
#         self.setupUi(self)

#         # 二维码
#         self.image: ClickableLabel = ClickableLabel()
#         self.image.setFixedSize(350, 350)
#         self.layout_qrcode.addWidget(self.image, alignment=Qt.AlignCenter)

#     def closeEvent(self, event) -> None:
#         try:
#             if self.check_login_thread.isRunning():
#                 # self.check_login_thread.terminate()
#                 self.is_ok = True
#                 self.check_login_thread.wait()
#                 print('stop check login status thread')
#         except:
#             pass
#         event.accept()
    
#     def showEvent(self, event) -> None:
#         print('show user window')
#         if self.mode == "login":
#             self.login()
#             event.accept()
#             return
#         if self.mode == "logout":
#             self.login_status = 1
#             self.is_ok = True
#             if not (self.user_info):
#                 self.user_info = login.get_user_info()
#                 print(f"get user info: {self.user_info}")
#             self.image.setPixmap(self.user_info["image"])
#             self.label.setText(f'欢迎, {self.user_info["name"]}')


def main() -> None:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()