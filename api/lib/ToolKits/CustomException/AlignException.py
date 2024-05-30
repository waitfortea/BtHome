class LenAlignError(Exception):
    def __init__(self):
        self.message=='对象长度不对齐'


class LengthOutofRange(Exception):
    def __init__(self):
        self.message='长度超过'