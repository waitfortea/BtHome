from ToolKits.CustomType import Type

def asyncTenthRepetition(func):
    async def wrapper(*args,**kwargs):
        count=0
        while True and count<10:
            try:
                result=await func(*args,**kwargs)
                return result
            except:
                count+=1
                print(f'重新连接{count}')
        raise Exception
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



