from dataclasses import dataclass
@dataclass()
class ProxyProcessor:
    proxy_aiohttp=None
    proxy_request=None
    proxy_status=False

globalProxy=ProxyProcessor()

def set():
    global proxy_aiohttp
    proxy_aiohttp="111"
def setProxy():
    global globalProxy
    globalProxy.proxy_aiohttp = "http://127.0.0.1:10809"
    globalProxy.proxy_request = {'http': "http://127.0.0.1:10809"
        , 'https': "http://127.0.0.1:10809"}
    globalProxy.proxy_status=True

def unsetProxy():
    global globalProxy
    globalProxy.proxy_aiohttp = None
    globalProxy.proxy_request = None
    globalProxy.proxy_status = False

