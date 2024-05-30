class NotFoundResponse(Exception):
    def __init__(self):
        self.message = '无响应'