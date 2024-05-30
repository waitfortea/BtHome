import asyncio
from abc import ABC,abstractmethod


def asyncStrategy(tasks):
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result=loop.run_until_complete(tasks)
        return result





