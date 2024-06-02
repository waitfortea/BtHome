
from ._CustomException import _CustomeException

class ContentBlankException(_CustomeException):
    def __init__(self, error_data=None):
        super().__init__()
        self.error_data = error_data
        self.error_name='对象内容为空'