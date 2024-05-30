import os

class ProxyProcessor:
    def setRequestProxy(self):
        os.environ["http_proxy"] = "http://127.0.0.1:10809"
        os.environ["https_proxy"] = "http://127.0.0.1:10809"

    @property
    def asyncProxy(self):
        return "http://127.0.0.1:10809"