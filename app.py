from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMetaType
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout
import sys
from module import func
from module import Ui_window
from module.main import download_video
import threading
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnimeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.page = 1
        self.ui = Ui_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        self.setup_connections()
        self.active_threads = []

    def setup_ui(self):
        """初始化UI设置"""
        self.setFixedSize(self.width(), self.height())
        self.center_window()
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_2.setText(str(self.page))
        self.ui.textBrowser.setOpenExternalLinks(True)
        self.cursor = self.ui.textBrowser.textCursor()

    def setup_connections(self):
        """设置信号连接"""
        self.ui.pushButton.clicked.connect(lambda: self.search(self.ui.lineEdit.text()))
        self.ui.pushButton_2.clicked.connect(self.previous_page)
        self.ui.pushButton_3.clicked.connect(self.next_page)
        self.ui.lineEdit.returnPressed.connect(lambda: self.search(self.ui.lineEdit.text()))

    def center_window(self):
        """将窗口居中显示"""
        frame = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def search(self, text: str, page: int = None) -> None:
        """搜索动漫并显示结果"""
        if not text.strip():
            logger.warning("搜索文本为空")
            self.ui.textBrowser.append("请输入搜索内容")
            return

        if page is not None:
            self.page = page
        self.ui.lineEdit_2.setText(str(self.page))

        try:
            data = func.get_base_url(text, self.page)
            if not data:
                logger.info("没有找到搜索结果")
                self.ui.textBrowser.append("未找到相关结果")
                return
            self.display_search_results(data)
        except Exception as e:
            logger.error(f"搜索出错: {str(e)}", exc_info=True)
            self.ui.textBrowser.append(f"搜索出错: {str(e)}")

    def display_search_results(self, data: List[Tuple[str, str]]) -> None:
        """显示搜索结果"""
        try:
            widget = QWidget()
            layout = QGridLayout()
            widget.setLayout(layout)

            for i, (url, title) in enumerate(data):
                btn = QPushButton(title)
                btn.clicked.connect(lambda checked, url=url: self.start_download(url))
                layout.addWidget(btn)

            self.ui.scrollArea.setWidget(widget)
        except Exception as e:
            logger.error(f"显示搜索结果时出错: {str(e)}", exc_info=True)
            self.ui.textBrowser.append("显示搜索结果时出错")

    def start_download(self, url: str) -> None:
        """启动下载线程"""
        try:
            thread = threading.Thread(
                target=self._download_wrapper,
                args=(url,)
            )
            thread.daemon = True
            self.active_threads.append(thread)
            thread.start()
            logger.info(f"开始下载: {url}")
        except Exception as e:
            logger.error(f"启动下载线程时出错: {str(e)}", exc_info=True)
            self.ui.textBrowser.append(f"启动下载失败: {str(e)}")

    def _download_wrapper(self, url: str) -> None:
        """下载包装器，处理异常"""
        try:
            download_video(url, self.ui.textBrowser, self.cursor)
        except Exception as e:
            logger.error(f"下载过程中出错: {str(e)}", exc_info=True)
            self.ui.textBrowser.append(f"下载出错: {str(e)}")
        finally:
            for thread in self.active_threads[:]:
                if not thread.is_alive():
                    self.active_threads.remove(thread)

    def next_page(self) -> None:
        """下一页"""
        self.page += 1
        self.search(self.ui.lineEdit.text(), self.page)

    def previous_page(self) -> None:
        """上一页"""
        if self.page > 1:
            self.page -= 1
            self.search(self.ui.lineEdit.text(), self.page)

    def closeEvent(self, event):
        """关闭窗口时等待所有下载完成"""
        for thread in self.active_threads:
            if thread.is_alive():
                thread.join(timeout=1.0)
        super().closeEvent(event)

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QMetaType.type("QTextCursor")
    app = QApplication(sys.argv)
    window = AnimeDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
