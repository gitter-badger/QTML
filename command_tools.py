"""PyQt5 Minecraft Launcher测试终端
其中提供了读取、修改的设置功能
"""
# 调整设置测试用
from settings import Setting

import os
import cmd
import sys

class Tools(cmd.Cmd):
    prompt = "> "
    doc_leader = __doc__
    text = """PyQt5 Minecraft Launcher Terminal
Type "help" for more information.
    """
    config = Setting("config")

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.do_title("PyQt5 Minecraft Launcher Terminal")
        print(self.text)

    def exit_terminal(self):
        sys.exit()

    def do_exit(self, arg: str):
        """退出终端
exit
"""
        self.exit_terminal()

    def do_quit(self, arg: str):
        """退出终端
exit
        """
        self.exit_terminal()

    def do_set(self, arg: str):
        """设置一个值
格式: set key value
        """
        exec_arg = arg.split()
        if len(exec_arg) != 2:
            print("输入格式错误")
            return
        key, value = exec_arg
        self.config.add(key, value)

    def do_del(self, arg: str):
        """删除一个值
del key
delete key
        """
        exec_arg = arg.split()
        if len(exec_arg) != 1:
            print("输入格式错误")
            return
        try:
            self.config.delete(exec_arg[0])
        except KeyError:
            print(f"值\"{exec_arg[0]}\"不存在")

    do_delete = do_del

    def do_title(self, title: str):
        """设置终端的题目
title {caption}
        """
        os.system(f"title {title}")

    def do_read(self, arg: str):
        """读取一个值
read key
read # 返回全部值
        """
        exec_arg = arg.split()
        if len(exec_arg) != 1 and len(exec_arg) != 0:
            print("输入格式错误")
            return
        if len(exec_arg) == 1:
            print(self.config.try_get(exec_arg[0], f"值\"{exec_arg[0]}\"不存在"))
        else:
            print(self.config.read())
    

def main():
    tools = Tools()
    tools.cmdloop()

if __name__ == "__main__":
    main()
