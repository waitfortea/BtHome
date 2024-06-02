from ._CustomException import _CustomeException


class FileNotFound(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name='文件不存在'
class DirNotFound(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = '文件夹不存在'
class FileFormatNotAlign(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name="文件格式错误"
class PathNotFound(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = '路径不存在'