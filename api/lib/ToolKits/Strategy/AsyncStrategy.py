import asyncio

def asyncStrategy(tasks):
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result=loop.run_until_complete(tasks)
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
