import os
import requests
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool, Qt
import time, video
from subprocess import check_output, DEVNULL, STDOUT

ffmpeg_path = "ffmpeg\\bin\\ffmpeg.exe"  # 设置ffmpeg的路径

class DownloadSignals(QObject):
    """ 定义信号 """
    progress = Signal(int)
    finished = Signal(str)
    paused = Signal()
    resumed = Signal()

class DownloadWorker(QRunnable):
    """ 下载工作线程 """
    global ffmpeg_path

    def __init__(self, bv: str, title: str = None, path: str = "video\\"):
        super().__init__()
        self.bv = bv
        self.url = f"https://www.bilibili.com/video/{bv}/"
        self.info = video.get_video_info(self.url)
        self.title = title if title else self.info["title"]
        self.save_path = path
        self.signals = DownloadSignals()
        self._is_paused = False  # 暂停标志

    @Slot()
    def run(self):
        # try:
        response1 = requests.get(self.info["audio_url"], stream=True, headers=video.headers)
        audio_length = response1.headers.get('content-length')
        response2 = requests.get(self.info["video_url"], stream=True, headers=video.headers)
        video_length = response2.headers.get('content-length')

        # 如果没有Content-Length头部
        if audio_length is None or video_length is None:
            with open(self.save_path + f"\\{self.bv}.mp3", 'wb') as f1:
                f1.write(response1.content)
            with open(self.save_path + f"\\{self.bv}.mp4", 'wb') as f2:
                f2.write(response2.content)
            return
        audio_length = int(audio_length)
        video_length = int(video_length)
        total_length = audio_length + video_length
        dl = 0

        # 下载音频
        with open(f"{self.save_path+self.bv}.mp3", 'wb') as f:
            for data in response1.iter_content(chunk_size=4096):
                while self._is_paused:  # 检查是否暂停
                    self.signals.paused.emit()  # 发送暂停信号
                    time.sleep(0.1)  # 等待一段时间后再次检查
                dl += len(data)
                f.write(data)
                self.signals.progress.emit(int(dl * 100 // total_length))  # 根据音频的进度发送信号

        # 下载视频
        with open(f"{self.save_path+self.bv}.mp4", 'wb') as f:
            for data in response2.iter_content(chunk_size=4096):
                while self._is_paused:  # 检查是否暂停
                    self.signals.paused.emit()  # 发送暂停信号
                    time.sleep(0.1)  # 等待一段时间后再次检查
                dl += len(data)
                f.write(data)
                self.signals.progress.emit(int(dl * 100 // total_length))
        check_output(f'{ffmpeg_path} -i "{self.save_path+self.bv}.mp4" -i "{self.save_path+self.bv}.mp3" -c:v copy -c:a copy "{self.save_path+self.title}.mp4"', shell=True, stderr=STDOUT)
        os.remove(f"{self.save_path+self.bv}.mp4")
        os.remove(f"{self.save_path+self.bv}.mp3")
        # os.rename(f"{self.save_path+self.bv}_ok.mp4", f"{self.save_path+self.title}.mp4")
        self.signals.finished.emit(f"完成：{self.save_path}")
        # except Exception as e:
        #     print(f"下载失败: {e}")
        #     self.signals.finished.emit(f"失败：{self.save_path}")

    def pause(self):
        """ 暂停下载 """
        self._is_paused = True
        self.signals.paused.emit()

    def resume(self):
        """ 恢复下载 """
        self._is_paused = False
        self.signals.resumed.emit()

class DownloaderApp(QWidget):
    def __init__(self, urls, base_dir):
        super().__init__()

        self.urls = urls
        self.base_dir = base_dir
        self.workers = []
        self.progress_bars = []

        self.initUI()
        self.start_downloads()

    def initUI(self):
        layout = QVBoxLayout()

        for i in range(len(self.urls)):
            h_layout = QHBoxLayout()
            label = QLabel(f"文件 {i+1}:")
            h_layout.addWidget(label)

            progress_bar = QProgressBar()
            progress_bar.setAlignment(Qt.AlignCenter)
            self.progress_bars.append(progress_bar)
            h_layout.addWidget(progress_bar)

            layout.addLayout(h_layout)

        self.pause_button = QPushButton("暂停所有")
        self.pause_button.clicked.connect(self.pause_all)
        layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("恢复所有")
        self.resume_button.clicked.connect(self.resume_all)
        layout.addWidget(self.resume_button)

        self.setLayout(layout)
        self.setWindowTitle("下载器")

    def start_downloads(self):
        thread_pool = QThreadPool.globalInstance()
        max_threads = min(50, thread_pool.maxThreadCount())
        thread_pool.setMaxThreadCount(max_threads)  # 设置最大线程数

        for i, url in enumerate(self.urls):
            worker = DownloadWorker(url)
            worker.signals.progress.connect(lambda value, idx=i: self.update_progress(value, idx))
            worker.signals.finished.connect(lambda msg: print(msg))
            worker.signals.paused.connect(lambda: print("下载已暂停"))
            worker.signals.resumed.connect(lambda: print("下载已恢复"))
            self.workers.append(worker)
            thread_pool.start(worker)

    def update_progress(self, value, index):
        self.progress_bars[index].setValue(value)

    def pause_all(self):
        for worker in self.workers:
            worker.pause()

    def resume_all(self):
        for worker in self.workers:
            worker.resume()

if __name__ == "__main__":
    urls = [
        "BV1jqtFedEbp",
        "BV1QgtVeDEbD"
    ]
    base_dir = "./downloads"  # 设置文件保存的基本目录
    os.makedirs(base_dir, exist_ok=True)  # 确保目录存在

    app = QApplication(sys.argv)
    ex = DownloaderApp(urls, base_dir)
    ex.show()
    sys.exit(app.exec_())