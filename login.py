from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QHBoxLayout
from PyQt5.QtCore import QUrl, QLocale, pyqtSignal
import minecraft_launcher_lib as mclib
import json
import sys
import os


CLIENT_ID = "dbb5fc17-43ac-4aa6-997e-ca69cde129a4"  # 请勿盗用
SECRET = "1bf7Q~nt2WVtYT4Oe9fj__jeXQE35HiYalI0E" # 请勿盗用
REDIRECT_URL = "https://login.microsoftonline.com/common/oauth2/nativeclient"


class LoginWindow(QWebEngineView):
    user = pyqtSignal(tuple) # 用户名, uuid, token


    def __init__(self):
        QWebEngineView.__init__(self)
        self.page().profile().cookieStore().deleteAllCookies() # 修复无法显示登录页面的bug

        # self.refresh_token_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "refresh_token.json")

        # if os.path.isfile(self.refresh_token_file):
        #     with open(self.refresh_token_file, "r", encoding="utf-8") as f:
        #         refresh_token = json.load(f)
        #         # Do the login with refresh token
        #         try:
        #             account_informaton = mclib.microsoft_account.complete_refresh(CLIENT_ID, SECRET, REDIRECT_URL, refresh_token)
        #             self.show_account_information(account_informaton)
        #             return
        #         except mclib.exceptions.InvalidRefreshToken:
        #             pass

        # Open the login url
        self.load(QUrl(mclib.microsoft_account.get_login_url(CLIENT_ID, REDIRECT_URL)))

        self.urlChanged.connect(self.new_url)

    def new_url(self, url: QUrl):
        if mclib.microsoft_account.url_contains_auth_code(url.toString()):
            auth_code = mclib.microsoft_account.get_auth_code_from_url(url.toString())
            account_informaton = mclib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL, auth_code)
            self.show_account_information(account_informaton)

    def show_account_information(self, information_dict):
        user_name = information_dict["name"]
        uuid = information_dict["id"]
        token = information_dict["access_token"]
        self.user.emit((user_name, uuid, token))

        # with open(self.refresh_token_file, "w", encoding="utf-8") as f:
        #     json.dump(information_dict["refresh_token"], f, ensure_ascii=False, indent=4)

class LoginDialog(QDialog):
    """增加一个Microsoft账户窗口"""

    user = pyqtSignal(str, str, str)

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("登录到Minecraft Java")
        QWebEngineProfile.defaultProfile().setHttpAcceptLanguage("-".join(QLocale.system().name().split("_"))) # 语言设置
        self.__layout = QHBoxLayout(self)
        self.login = LoginWindow()
        self.__layout.addWidget(self.login)
        self.setLayout(self.__layout)
        self.login.user.connect(self.__done)

    def __done(self, u: tuple):
        self.user.emit(u[0], u[1], u[2])
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    LoginDialog().exec_()
