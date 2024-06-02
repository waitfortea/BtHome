from ._CustomException import _CustomeException

class LenAlignError(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = "长度不一致"
class OutofRange(_CustomeException):
    def __init__(self, erro_data=None):
        super().__init__()
        self.erro_data = erro_data
        self.error_name = "超出范围"