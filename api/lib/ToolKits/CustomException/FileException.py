class ContentBlankException(Exception):
    def __init__(self):
        self.message='对象内容为空'