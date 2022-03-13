# gui部分
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QPushButton, QApplication, QListWidget, QAction, QMenuBar, QSizePolicy, QVBoxLayout, QHBoxLayout, QTextBrowser, QLabel, QMessageBox, QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QCloseEvent, QPaintEvent, QPainter, QPixmap, QColor, QBrush, QPainterPath, QFont, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QRectF, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView

from game import MinecraftJava, get_mc_version, launch, window_launch
from login import LoginDialog
from settings import BASE_DIR, Setting, get_default_mc_floor, get_mc_floor, get_qtml_mc_floor, get_style
from language import _

from ctypes import cdll
from ctypes.wintypes import HWND

import os
import sys


BUTTON_HEIGHT = 30  # 按钮高度
BUTTON_WIDTH = 30  # 按钮宽度
TITLE_HEIGHT = 30  # 标题栏高度

__version__ = "1.0"

info = """<h1>重要信息</h1>
<pre>
1. Mojang账户已经和我们说拜拜了, 请立刻迁移到微软账户
2. 我们改为免费制, 请支持我们继续开发 (https://afdian.net/@chenmy1903)
</pre>
<h1>更新日志</h1>
<pre>
<h5>1.0</h5>
1. 之前的版本因为做的太烂, 所以删了
2. 更换源, 不再是龟速下载 (指之前的一个小时下载一个游戏版本)
3. 登录机制完善 (不会出现语言错误和显示白窗口的错误)
4. 可以保存上次窗口的大小
</pre>
"""

class DownloadWidget(QWidget):
    """下载组件"""
    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.__layout = QHBoxLayout(self)
        self.list = QListWidget(self)
        self.setLayout(self.__layout)
        

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("\n")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.config = Setting("config")
        self.tab = QTabWidget()
        self.setCentralWidget(self.tab)
        self.information = QTextBrowser(self)
        self.information.setHtml(info)
        self.download = DownloadWidget()
        self.tab.addTab(self.information, _("重要信息"))
        self.tab.addTab(self.download, _("下载"))
        self.tab.setStyleSheet("color:#f1f1f1;")
        self.init_window_size()
        self.setWindowOpacity(0.9)
        self.setAttribute(Qt.WA_TranslucentBackground)
        hWnd = HWND(int(self.winId()))
        cdll.LoadLibrary(os.path.join(BASE_DIR, "dll", "aeroDll.dll")).setBlur(hWnd)
        with open(os.path.join(BASE_DIR, "style.qss"), "r") as f:
            self.setStyleSheet(f.read())
        self.__set_style()
        self.tab.currentChanged.connect(self.__set_style)

    def __set_style(self):
        w = self.tab.currentWidget()
        w.setStyleSheet("color:#f1f1f1;")

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap(os.path.join(BASE_DIR, "background", "bg.png"))
        painter.drawPixmap(self.rect(), pixmap)


    def init_window_size(self):
        """设置窗口大小"""
        w, h = self.config.null_add("size", (800, 600))
        self.resize(w, h)

    def closeEvent(self, a0: QCloseEvent) -> None:
        if QMessageBox.question(self, _("退出"), _("确认退出QTML?")) == QMessageBox.Yes:
            self.config.add("size", (self.width(), self.height()))
            a0.accept()
        else:
            a0.ignore()

def show():
    app = QApplication(sys.argv)
    app.setStyle(get_style())
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    show()
