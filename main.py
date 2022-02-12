# QTML的主程序
# 其中使用的Setting类的说明请看https://chenmy1903.github.io/wang250/mods/make_mod/

import os
import sys
import webbrowser

from pickleshare import PickleShareDB
from PyQt5.QtWidgets import QWidget, QMainWindow, QFrame, QTabWidget, QPushButton, QLineEdit, QScroller, QLabel, QMessageBox, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QUrl

__version__ = "1.0"  # 版本号

adout_text = f"""
<h1>关于PyQt5 Minecraft Launcher</h1>
版本号：{__version__}<br>
<h2>作者: </h2>
<a href="http://chenmy1903.tk/">chenmy1903(鸭皇)</a><br>
<a href="http://qtml.chenmy1903.tk/">QTML</a><br>
<h2>本项目完全开源</h2>
<a href="https://afdian.net/@duck_chenmy1903/">赞助我, 让我做出更好的产品</a><br>
<a href="http://qtml.chenmy1903.tk/github">或许你也可以加入到我们</a><br>
<a href="https://github.com/chenmy1903/QTML/">去我们的Github仓库逛逛</a><br>
<h2>感谢以下的开源项目</h2>
<a href="https://www.python.org">Python</a><br>
<a href="https://pypi.org/project/PyQt5/">PyQt5</a><br>
"""


class Setting:
    def __init__(self, file_name, config={}, config_path="~/.duck_game/QTML"):
        super().__init__()
        self.file_name = file_name
        self.db = PickleShareDB(config_path)
        if file_name not in self.db:
            self.db[file_name] = config

    def add(self, key, value):
        """添加新值"""
        new = self.db[self.file_name]
        new[key] = value
        self.db[self.file_name] = new

    def read(self, config=None):
        """读文件"""
        if config:
            return self.db[self.file_name][config]
        return self.db[self.file_name]

    def delete(self, value: str):
        """删除某个值"""
        config = self.db[self.file_name]
        del config[value]
        self.db[self.file_name] = config

    def try_get(self, key: str, defacult=None):
        """尝试获取某个值"""
        return self.read(key) if key in self.read() else defacult

    def null_add(self, key: str, value: str = None):
        """不存在则添加某个值"""
        tryg = self.try_get(key)
        if tryg == None:
            self.add(key, value)
        return tryg if tryg else value

def is_url(url: str):
    return url.startswith("https://") or url.startswith("http://")

class LoginWidget(QWidget):
    """正版登录组件"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)

class DownloadWidget(QWidget):
    """下载游戏组件"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)

class AboutWidget(QWebEngineView):
    """关于QTML"""
    windows = []

    def __init__(self, parent: QWidget = None):
        QWebEngineView.__init__(self, parent)
        self.setHtml(adout_text)
        self.urlChanged.connect(self.open_page)

    def open_page(self, url: QUrl):
        if not is_url(url.toString()):
            return
        if QMessageBox.question(self, "警告", "即将离开QTML, 是否打开链接?") == QMessageBox.Yes:
            webbrowser.open(url.toString())
        self.setHtml(adout_text)

class GameSettingWidget(QWidget):
    """游戏设置"""

    


class SettingWidget(QTabWidget):
    """设置启动器组件"""

    def __init__(self, parent: QWidget = None):
        QTabWidget.__init__(self, parent)
        self.setTabPosition(self.West)
        self.addTab(GameSettingWidget(), "配置启动选项")
        self.addTab(AboutWidget(), "关于")
        

class QTMLMainWidget(QTabWidget):
    
    def __init__(self, parent: QWidget = None):
        QTabWidget.__init__(self, parent)
        self.addTab(LoginWidget(), "登录")
        self.addTab(DownloadWidget(), "下载")
        self.addTab(SettingWidget(), "设置")



class QTMLWindow(QMainWindow):
    """主窗口"""

    def __init__(self, parent: QWidget = None):
        QMainWindow.__init__(self, parent)
        self.config = Setting("config")
        self.inst_path = self.get_inst_path()
        self.setWindowTitle(self.get_title())
        self.setWindowIcon(QIcon(os.path.join(self.inst_path, "icon.ico")))
        self.setCentralWidget(QTMLMainWidget())

    def get_inst_path(self):
        """获取游戏安装目录"""
        setup_file = Setting("setup")
        return setup_file.read("path")

    def get_title(self):
        """获取窗口的题目"""
        return self.config.try_get("title", "PyQt5 Minecraft Launcher")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    widget = QTMLWindow()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
