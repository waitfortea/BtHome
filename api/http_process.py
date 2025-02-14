from api.lib.ToolKits.RequestsProcess import  *
from api.lib.ToolKits.Proxy import *
from api.lib.Config import *
from api.lib.brower import *
import asyncio
globalProxy.proxy_aiohttp = {'http': config['proxy']['proxy_aiohttp']}
globalProxy.proxy_request = {'http':config['proxy']['proxy_request'],'https':config['proxy']['proxy_request']}


__all__ = 'gethtml','request_hmtl_strategy','aiohttp_html_strategy','async_httpx_html_strategy','drssionpage_brower_html_strategy'

def request_hmtl_strategy(url,type = 'get',**kwargs)->str:


    return RequestsProcessor(session = requestSession,url = url ,proxies = globalProxy.get_proxy('request'),**kwargs).text(type)

def aiohttp_html_strategy(url,type = 'get',**kwargs):
    """

    :param kwargs:
    :return: coroutine
    """

    return  AiohttpProcessor(session=aiohttpSession,url = url,proxy=globalProxy.get_proxy('aiohttp'),**kwargs).text(type)

def async_httpx_html_strategy(url,type = 'get',**kwargs):
    """

        :param kwargs:
        :return: coroutine
        """
    if globalProxy.proxy_status:
        asyncHttpxSession = httpx.AsyncClient(timeout=50,proxies= globalProxy.get_proxy('request'))
    else:
        asyncHttpxSession = httpx.AsyncClient(timeout=50)

    return AiohttpProcessor(session=asyncHttpxSession, url = url,**kwargs).text(type)

def drssionpage_brower_html_strategy(url,**kwargs)->str:
    tab = global_brower.create_tab(url)
    html = tab.html
    return html


def gethtml(url,strategy=drssionpage_brower_html_strategy,*args,**kwargs):
    return async_strategy(strategy(url,*args,**kwargs))