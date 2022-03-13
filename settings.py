from pickleshare import PickleShareDB

import psutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

def install_path():
    """获取QTML安装目录"""
    config = Setting("setup")
    return config.try_get("path", BASE_DIR)

def get_qtml_mc_floor():
    """获取QTML的Minecraft安装目录"""
    mc = os.path.join(install_path(), ".minecraft")
    if not os.path.isdir(mc):
        os.makedirs(mc)
    return mc

def get_default_mc_floor():
    """获取官方启动器的Minecraft安装目录"""
    mc = os.path.join(os.path.expandvars("%APPDATA%"), ".minecraft")
    if not os.path.isdir(mc):
        os.makedirs(mc)
    return mc

def get_ram_size():
    """获取给JVM虚拟的的内存"""
    config = Setting("config")
    return config.null_add("jvm_ram", int(round((float(psutil.virtual_memory().total) / 1024 / 1024 / 1024), 2) // 2))

def get_mc_floor():
    """获取配置文件中的Minecraft目录"""
    config = Setting("config")
    return config.null_add("mc-floor", get_qtml_mc_floor())

def get_style():
    """获取UI主题
总共4种 ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
请不要使用主题 WindowsXP和WindowsVista, 这会出现很大的bug
    """
    config = Setting("config")
    return config.null_add("window_style", "Fusion")

if __name__ == "__main__":
    config = Setting("config")
    print(config.read())
    config.delete("jvm_ram")
