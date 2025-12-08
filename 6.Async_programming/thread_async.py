import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def check_stock(item):
    print(f"Checking {item} in store...")
    time.sleep(3) # Blocking operation
    return f"{item} stock 42"

async def main():
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=2) as pool:
        # result = await loop.run_in_executor(pool, check_stock, "Masala chai")
        result,result2= await asyncio.gather(
            loop.run_in_executor(pool, check_stock, "Masala chai"),
            loop.run_in_executor(pool, check_stock, "Ginger chai")
        )
        print(result)
        print(result2)

asyncio.run(main())