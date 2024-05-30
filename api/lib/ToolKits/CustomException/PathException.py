class FileNotFound(Exception):
    def __init__(self):
        self.message='文件不存在'
class DirNotFound(Exception):
    def __init__(self):
        self.message = '文件夹不存在'
class FileFormatNotAlign(Exception):
    def __init__(self):
        self.message="文件格式错误"
class PathNotFound(Exception):
    def __init__(self):
        self.message = '路径不存在'