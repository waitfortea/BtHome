class TypeError(Exception):
    def __init__(self):
        self.message='数据类型不符'

class TypeAlignError(Exception):
    def __init__(self):
        self.message='对象类型不一致'

class GeneratedError(Exception):
    def __init__(self):
        self.message='不可迭代'


class InitFailedError(Exception):
    def __init__(self):
        self.message = '初始化失败'

