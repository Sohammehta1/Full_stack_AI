# async def -> declares a coroutine
# coroutine: a special function that can be paused
# await: Pauses the execution until the result is ready.
# Event loop: The engine that runs and scheduls coroutines in python

import asyncio


async def brew(name):
    print(f"Brewing {name}...")
    await asyncio.sleep(2)
    print(f'{name} is ready.')

async def serve():
    await asyncio.gather(
        brew("masala chai"),
        brew("ginger chai")
    )

asyncio.run(serve())

# The above is a non blocking operation
# so whenever the flow hits the await statement, interpreter tries to execute the remaining tasks