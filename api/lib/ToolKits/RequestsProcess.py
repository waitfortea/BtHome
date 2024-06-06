import re
from dataclasses import dataclass
import requests
import aiohttp
import time
import atexit
from .Strategy.AsyncStrategy import asyncStrategy
from .Event import *
from .CustomException import *
from .CustomDecorator import *
#data对应请求体，如果请求体是json,也可以用json表示
#params对应post\get请求参数]


async def createSession():
    return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(connect=5,total=10))
async def close():
    await aiohttpSession.close()
    time.sleep(1)

def closeSession():

    asyncStrategy(close())

requestSession=requests.session()
aiohttpSession=asyncStrategy(createSession())
atexit.register(closeSession)

@dataclass
class RequestsProcessor:
    def __init__(self, url,**kwargs):
        self.url = url
        self.session =requests.session()
        self.kwargs = kwargs

    @tenthRepetition
    def response(self,type='get'):
        try:
            if type=='get':
                response= self.session.get(self.url, **self.kwargs)
            else:
                response=  self.session.post(self.url, **self.kwargs)
            callEvent("logNetWork", {"type": type, "requestURL": self.url, "responseURL": response.url,"proxy":self.kwargs['proxies']})
            return response
        except Exception as e:
            print(e)
            raise NotFoundResponse(self.url)


    def content(self,type='get'):

        return self.response(type).content

    def text(self,type='get'):
        return self.response(type).text


    def status(self,type='get'):
        return self.response(type).status_code


    def requestHeaders(self,type='get'):
        return self.response(type).headers



@dataclass
class AsyncRequestsProcessor:

    def __init__(self,url,session,**kwargs):
        self.session=session
        self.url = url
        self.kwargs = kwargs


    async def response(self,type='get'):
        try:
            if type=='get':
                response = await  self.session.get(self.url, **self.kwargs)
            else:
                response = await  self.session.post(self.url, **self.kwargs)

            callEvent("logNetWork",{"type":type,"requestURL":self.url,"responseURL":response.url,"proxy":self.kwargs['proxy']})

            return response
        except Exception as e:
            print(e)
            raise NotFoundResponse(self.url)

    async def content(self,type='get'):
        response = await self.response(type)
        text = await response.contet.read()
        return text
    
    async def text(self,type='get'):
        response=await self.response(type)
        text= await response.text()
        return text
    
    async def status(self,type='get'):
        response = await self.response(type)
        text = await response.status
        return text

    async def headers(self,type='get'):
        response = await self.response(type)
        headers = await response.headers
        return headers

def getResFileSuffix(res):
    content_disposition= res.headers.get('content-disposition')
    # breakpoint()
    if content_disposition is None:
        suffix=re.search("\.[^.]*$",str(res.url)).group()
        return suffix
    else:
        fileName=content_disposition.split('filename=')[1].strip('"')
        suffix = re.search("\.[^.]*$", fileName).group()
        return suffix



