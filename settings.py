from pickleshare import PickleShareDB

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
