from .CustomException import *

def asyncRetry(func):
    async def wrapper(*args,**kwargs):

        repeat=1 if "retry" not in kwargs.keys() else kwargs["retry"]
        kwargs.pop("retry",None)
        count=0
        while True :
            try:
                result=await func(*args,**kwargs)
                return result
            except Exception as e:
                print(e)
                count+=1
                print(f'重新连接{count}')
                if count>repeat-1:
                    raise NotFoundResponse
    return wrapper

def tenthRepetition(func):
    def wrapper(*args,**kwargs):
        count=0
        while True and count<10:
            try:
                result=func(*args,**kwargs)
                return result
            except:
                count+=1
                print(f'重新连接{count}')
        raise Exception
    return wrapper



