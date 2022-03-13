# QTML游戏部分
import os
import subprocess
import minecraft_launcher_lib as mclib
import configparser
from settings import get_mc_floor, get_ram_size
from language import _

import uuid
import json

false = "false"
true = "true"

class FloorConfig(object):
    """游戏文件夹设置"""

    def __init__(self, floor: str):
        self.config = configparser.ConfigParser()
        self.ini = os.path.join(floor, "qtml.ini")
        self.config.read(self.ini)
    
    def set_value(self, section: str, key: str = None, value: str = None):
        """设置一个值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        if key and value:
            self.config.set(section, key, value)
        elif not all([key, value]) and (key != None or value != None):
            raise KeyError("No key or value.")
        with open(self.int, "w") as f:
            self.config.write(f)

    def read_all(self):
        """读取全部内容"""
        ref = {}
        for s in self.config.sections():
            ref[s] = {}
            for i in self.config.items(s):
                ref[s].update({i[0]: i[1]})
        return ref

class MinecraftJava(object):
    """后面还会对基岩版进行支持, 所以定义了一个类"""

    status: str = ""  # 状态
    progress: float = 0  # 当前任务进度
    maximum: int = 0  # 当前任务的所有文件

    def __init__(self, version: str, version_name: str):
        """初始化
version: [安装]安装的Minecraft版本
version_name: [名称]安装的Minecraft的名称, 以及启动时调用的jar包
        """
        object.__init__(self)
        self.version = version
        self.version_name = version_name
        self.launch_name = _("qtml我的世界Java版启动器")  # 启动器名称
        self.callback = {
            "setStatus": self.__set_status,
            "setProgress": self.__set_progress,
            "setMax": self.__set_maximum
        }

    def __set_status(self, text: str):
        """设置状态(私有)"""
        self.status = text
    
    def __set_progress(self, progress: float):
        """设置当前任务进度(私有)"""
        self.progress = round(progress / self.maximum, 2)
    
    def __set_maximum(self, maximum: int):
        """设置总共任务进度(私有)"""
        self.maximum = maximum

    def install_minecraft(self, forge: bool = False, fabric: bool = False):
        """下载Minecraft Java主体"""
        if forge:
            self.install_forge()
        elif fabric:
            self.install_fabric()
        else:
            mclib.install.install_minecraft_version(
                self.version,
                get_mc_floor(),
                version_name=self.version_name, 
                callback=self.callback
            )

    def install_forge(self, forge_version: str = None):
        """安装Minecraft Forge
tip: 不需要执行这个, 去install_minecraft中把参数forge设置为True即可实现自动安装
        """
        if not forge_version:
            forge_version = self.get_forge_versions()[0]
        mclib.forge.install_forge_version(forge_version, get_mc_floor(), version_name=self.version_name, callback=self.callback)

    def install_fabric(self):
        """安装Minecraft Fabric
tip: 不需要执行这个, 去install_minecraft中把参数fabric设置为True即可实现自动安装"""
        mclib.fabric.install_fabric(self.version, get_mc_floor(), version_name=self.version_name, callback=self.callback)

    def get_forge_versions(self):
        """获取适合当前版本的Forge版本"""
        all_versions = mclib.forge.find_forge_version(self.version).split(" ")
        return all_versions

    def get_command(self, player: dict, options: dict = {}):
        """获取启动选项"""
        options.update(player)
        options["jvmArguments"] = [f"-Xmx{get_ram_size()}G", f"-Xms{get_ram_size()}G"]
        floor_config = self.read_floor_config()
        if floor_config["game"]["version-isolation"] == true:
            options["gameDirectory"] = os.path.join(get_mc_floor(), "versions", self.version_name)
        options["width"] = int(floor_config["size"]["width"])
        options["height"] = int(floor_config["size"]["height"])
        command = mclib.command.get_minecraft_command(self.version_name, get_mc_floor(), options)
        return command

    def read_floor_config(self):
        ref = {}
        floor = get_mc_floor()
        ini = os.path.join(floor, "qtml.ini")
        config = configparser.ConfigParser()
        if not os.path.isfile(ini):
            open(ini, "w").close()
            self.__init_floor_config(config)
        config.read(ini)
        for s in config.sections():
            ref[s] = {}
            for i in config.items(s):
                ref[s].update({i[0]: i[1]})
        return ref


    def __init_floor_config(self, config: configparser.ConfigParser):
        floor = get_mc_floor()
        ini = os.path.join(floor, "qtml.ini")
        config.add_section("game")
        config.set("game", "version-isolation", false)  # 版本隔离
        config.add_section("size")
        config.set("size", "width", "400")  # 长
        config.set("size", "height", "600")  # 高
        with open(ini, "w") as f:
            config.write(f)
    
    def get_demo_command(self):
        """获取测试版启动选项
        1. 适合整活
        2. 独家功能, 其他启动器没有(除了官启)
        """
        mc_uuid = str(uuid.uuid4())
        command = self.get_command({"username": "Player", "uuid": mc_uuid, "token": ""}, {"demo": True})
        return command

    def get_release_versions(self):
        """获取所有正式版本"""
        versions = mclib.utils.get_version_list()
        v_list = []
        for v in versions:
            if v["type"] == "release":
                v_list.append(v["id"])
        return v_list

    def get_snapshot_versions(self):
        """获取所有快照版本"""
        versions = mclib.utils.get_version_list()
        v_list = []
        for v in versions:
            if v["type"] == "snapshot":
                v_list.append(v["id"])
        return v_list

    def get_old_versions(self):
        """获取所有远古版本"""
        versions = mclib.utils.get_version_list()
        v_list = []
        for v in versions:
            if v["type"] == "old_alpha":
                v_list.append(v["id"])
        return v_list


def launch(command: list):
    """启动游戏"""
    subprocess.call(command)

def window_launch(command: list):
    """使用javaw.exe启动"""
    command[0] = os.path.join(os.path.dirname(command[0]), "javaw.exe")
    launch(command)

def get_mc_version(version_name: str, path: str):
    """获取一个Minecraft游戏的版本"""
    with open(os.path.join(path, "versions", version_name, f"{version_name}.json"), "r") as f:
        data = json.loads(f.read())
    return data["id"]
