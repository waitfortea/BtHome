import asyncio
import requests
from dataclasses import dataclass
import aiohttp
from Strategy.GeneralStrategy import asyncStrategy

#data对应请求体，如果请求体是json,也可以用json表示
#params对应post\get请求参数
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
        if type == 'get':
            return self.session.get(self.url, **self.kwargs).content
        else:
            return self.session.post(self.url, **self.kwargs).content


    def text(self,type='get'):
        if type == 'get':
            return self.session.get(self.url, **self.kwargs).text
        else:
            return self.session.post(self.url, **self.kwargs).text


    def status(self,type='get'):
        if type == 'get':
            return self.session.get(self.url, **self.kwargs).status_code
        else:
            return self.session.post(self.url, **self.kwargs).status_code


    def requestHeaders(self,type='get'):
        if type == 'get':
            return self.session.get(self.url, **self.kwargs).headers

        else:
            return self.session.post(self.url, **self.kwargs).headers



@dataclass
class AsyncRequestsProcessor:

    def __init__(self,url,session,**kwargs):
        self.session=session
        self.url = url
        self.kwargs = kwargs

    async def response(self):
        response=await  self.session.get(self.url,**self.kwargs)
        return response

    async def content(self,type='get'):
        if type=='get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        content =await response.content.read()
        return content
    
    async def text(self):
        if type == 'get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        text= await response.text()
        return text
    
    async def status(self):
        if type == 'get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        status =await response.status
        return status

    async def headers(self):
        if type == 'get':
            response = await  self.session.get(self.url, **self.kwargs)
        else:
            response = await  self.session.post(self.url, **self.kwargs)
        headers = await response.headers
        return headers

async def test():
    async with aiohttp.ClientSession() as session:
        text=await AsyncRequestsProcessor('https://www.btbtt15.com',session=session).text()
        print(text)
if __name__=='__main__':
    asyncStrategy(test())