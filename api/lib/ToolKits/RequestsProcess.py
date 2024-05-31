import asyncio
import time

import requests
from dataclasses import dataclass
import aiohttp
from .Strategy.AsyncStrategy import asyncStrategy
from .Event import *
#data对应请求体，如果请求体是json,也可以用json表示
#params对应post\get请求参数]
async def createSession():
    return aiohttp.ClientSession()

def closeSession(session):
    async def close():
        await session.close()
    asyncStrategy(close())

requestSession=requests.session()
aiohttpSession=asyncStrategy(createSession())

@dataclass
class RequestsProcessor:
    def __init__(self, url,**kwargs):
        self.url = url
        self.session =requests.session()
        self.kwargs = kwargs

    def response(self,type='get'):
        if type=='get':
            return self.session.get(self.url, **self.kwargs)
        else:
            return self.session.post(self.url, **self.kwargs)


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
        if type=='get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        callEvent("logNetWork",{"type":type,"requestURL":self.url,"responseURL":response.url})
        return response

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
        if type == 'get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        headers = await response.headers
        return headers


