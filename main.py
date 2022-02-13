# QTML的主程序
# 其中使用的Setting类的说明请看https://chenmy1903.github.io/wang250/mods/make_mod/
#
# 如果参与了开发，可以直接将自己的GitHub账号添加下面的感谢名单(支持Html)
# 只有参与开发的玩家才可以不捐款, 直接把自己的账号添加到感谢名单中
# 开发时不能自己把他人的账号添到感谢名单中，除非作者同意你这么做
# 必须做出贡献(开发)才可以免费添加到感谢名单中

import importlib
import os
import sys
import webbrowser

from PyQt5.QtWidgets import QWidget, QMainWindow, QFrame, QTabWidget, QPushButton, QLineEdit, QScroller, QLabel, QMessageBox, QApplication, QGridLayout, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QUrl

from settings import Setting

__version__ = "1.0"  # 版本号

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

adout_text = f"""
<h1>关于PyQt5 Minecraft Launcher</h1>
版本号: {__version__}<br>
<h2>作者: </h2>
<a href="http://chenmy1903.tk/">chenmy1903(鸭皇)</a><br>
<a href="http://qtml.chenmy1903.tk/">QTML</a><br>
<h2>本项目完全开源</h2>
<a href="https://afdian.net/@duck_chenmy1903/">赞助我, 让我做出更好的产品</a><br>
<a href="http://qtml.chenmy1903.tk/github">或许你也可以加入到我们</a><br>
<a href="https://github.com/chenmy1903/QTML/">去我们的Github仓库逛逛</a><br>
<h2>感谢以下的开源项目</h2>
<pre>
<a href="https://www.python.org">Python</a>
<a href="https://pypi.org/project/PyQt5/">PyQt5</a>
<a href="https://pypi.org/project/PickleShare/">PickleShare</a>
</pre>
<h2>此版本更新了什么</h2>
<pre>
1. 基础的GUI
2. 开始公测了
</pre>
"""

about_player_names = [
    "<a href=\"http://nkwjg.chenmy1903.tk\">nkwjg</a>", # 这是一个示例, 这就是作者
] # 感谢名单




def is_url(url: str):
    return url.startswith("https://") or url.startswith("http://")

class LoginWidget(QWidget):
    """正版登录组件"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.__layout = QGridLayout()
        if not get_activate():
            self.activate = QTextBrowser(self)
            self.activate.setHtml("""<h1>这是一个提示</h1>
<h2>你需要在爱发电页面进行赞助才可以去掉这个提示</h2>
<label>如果你有激活码, 可以前往设置-激活认证解除这个提示</label>        
""")
            self.__layout.addWidget(self.activate, 0, 1) # 作者也是要吃饭的
        self.setLayout(self.__layout)

class DownloadWidget(QWidget):
    """下载游戏组件"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)

class AboutWidget(QWebEngineView):
    """关于QTML"""

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

    pass

def get_activate():
    config = Setting("config")
    return importlib.import_module("activate_code").chack(config.try_get("activate"))

class ActivateWidget(QWidget):
    """激活码"""
    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.config = Setting("config")
        self.unlock_code = QLineEdit(self)
        self.unlock_code.setPlaceholderText("在此处输入在爱发电获取的激活码")
        self.unlock_button = QPushButton("激活QTML", self)
        self.unlock_button.clicked.connect(self.unlock)
        self.__layout = QGridLayout()
        self.__layout.addWidget(QLabel("输入激活码: ", self), 0, 0)
        self.__layout.addWidget(self.unlock_code, 0, 1)
        self.__layout.addWidget(self.unlock_button, 1, 1)
        self.setLayout(self.__layout)

    def unlock(self):
        """内部成员都不知道解锁码是多少"""
        if self.config.try_get("activate"):
            QMessageBox.information(self, "提示", "已经是激活状态了")
            return
        code = self.unlock_code.text()
        qtml_library = importlib.import_module("activate_code")
        if qtml_library.chack(code):
            self.config.add("activate", code)
            QMessageBox.information(self, "恭喜", "恭喜你, 解锁了QTML的完整版, 重启启动器生效")
        else:
            QMessageBox.information(self, "代码被古振兴抄走啦", "激活码错误")


class AboutPlayer(QWebEngineView):
    """感谢页面"""
    about_text = """<h1>感谢以下玩家对我们的支持</h1>
<pre>
{}
</pre>
""".format("\n".join(about_player_names))

    def __init__(self, parent: QWidget = None):
        QWebEngineView.__init__(self, parent)
        self.setHtml(self.about_text)
        self.urlChanged.connect(self.open_page)

    def open_page(self, url: QUrl):
        if not is_url(url.toString()):
            return
        self.setHtml(self.about_text)
        if QMessageBox.question(self, "警告", "即将离开QTML, 是否打开链接?") == QMessageBox.Yes:
            webbrowser.open(url.toString())

class QQWidget(QTextBrowser):
    """加入QQ"""

    def __init__(self, parent: QWidget = None):
        QTextBrowser.__init__(self, parent)
        self.config = Setting("config")
        self.setHtml(f"""<h1>加入QQ群</h1>
激活QTML之后请加入这个群, 验证码为下面的这个和￥20的激活码<br>
{self.config.try_get("activate", '检测到你使用破解版, 所以不予显示')}<br>
群号: 585830974<br>
输入格式: 激活码1激活码2
        """)


class SettingWidget(QTabWidget):
    """设置启动器组件"""

    def __init__(self, parent: QWidget = None):
        QTabWidget.__init__(self, parent)
        self.config = Setting("config")
        self.setTabPosition(self.West)
        self.addTab(GameSettingWidget(), "配置启动选项")
        if not get_activate():
            self.addTab(ActivateWidget(), "激活认证")
        else:
            self.addTab(QQWidget(), "加入QQ群")  
        self.addTab(AboutPlayer(), "感谢名单")
        self.addTab(AboutWidget(), "关于")
        

class QTMLMainWidget(QTabWidget):
    
    def __init__(self, parent: QWidget = None):
        QTabWidget.__init__(self, parent)
        self.addTab(LoginWidget(), "登录/启动")
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
    sys.path.append(BASE_DIR)
    app = QApplication(sys.argv)
    widget = QTMLWindow()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
