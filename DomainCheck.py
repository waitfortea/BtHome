
import ToolKits.RequestsProcess as RP
import aiohttp
import asyncio
from ToolKits.GeneralStrategy import AsyncStrategy

proxy_aiohttp=None
proxy_request=None

async def domain_check(path=None):

    with open('H:/app/bt-video/bt_domain.txt', 'r') as f:
        domain_list = f.read().strip().split('\n')
        f.close()

    async with aiohttp.ClientSession() as session:
        # 根据条件循环注册任务
        # 以下代码的结果就是
        if path is None:
            tasks = [asyncio.create_task(RP.AsyncRequestsProcessor(url=i, session=session,proxy=proxy_aiohttp).response()) for i in domain_list]
        else:
            tasks = [asyncio.create_task(RP.AsyncRequestsProcessor(url=i+'/'+path, session=session,proxy=proxy_aiohttp).response()) for i in domain_list]
        exception_num = 0
        while True:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for d in done:
                if d.exception() or d.result().status!=200:
                    exception_num += 1
                else:
                    check_result=str(d.result().url)
            if exception_num > 0:
                tasks = pending
                exception_num = 0
            else:
                for p in pending:
                    p.cancel()
                break
        await session.close()
    print(f'可用域名:{check_result}')
    await asyncio.sleep(2)
    return check_result

try:
    domain=AsyncStrategy().execute(domain_check())
except Exception as e:
    proxy_aiohttp = "http://127.0.0.1:10809"
    proxy_request = {'http': "http://127.0.0.1:10809"
        , 'https': "http://127.0.0.1:10809"}
    domain = AsyncStrategy().execute(domain_check())

if __name__ == '__main__':
    AsyncStrategy().execute(domain_check())