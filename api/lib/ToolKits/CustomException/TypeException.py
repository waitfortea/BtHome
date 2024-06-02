from ._CustomException import _CustomeException

class TypeError(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = "类型不一致"

class GeneratedError(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = "非迭代对象"

class InitFailedError(_CustomeException):
    def __init__(self,erro_data=None):
        super().__init__()
        self.erro_data=erro_data
        self.error_name = "初始化失败"

if __name__=="__main__":
    raise InitFailedError("s")


