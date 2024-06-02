__all__='asyncStrategy','firstComplete','allComplete'

import asyncio
import time

loop=asyncio.get_event_loop()

def asyncStrategy(tasks):
    global loopCount
    time.sleep(2)
    result = loop.run_until_complete(tasks)
    return result

async def firstComplete(tasks):
        result=""
        while not result:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for d in done:
                if d.exception():
                    pass
                else:
                    result=d.result()
                    for p in pending:
                        p.cancel()
                    break
            tasks=pending
        return result

async def allComplete(tasks):
    result_List=await asyncio.gather(*tasks)
    return result_List