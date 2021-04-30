import asyncio


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)