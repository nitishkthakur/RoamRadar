import asyncio
import httpx
import time

async def fetch_async(client, url, idx, t0):
    print(f"Task {idx} START  @ {time.time() - t0:.2f}s")
    await client.get(url)
    print(f"Task {idx} END    @ {time.time() - t0:.2f}s")

async def main():
    t0 = time.time()
    timeout = httpx.Timeout(10.0, connect=5.0, read=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        await asyncio.gather(
            fetch_async(client, "https://httpbin.org/delay/2", 1, t0),
            fetch_async(client, "https://httpbin.org/delay/2", 2, t0),
            fetch_async(client, "https://httpbin.org/delay/2", 3, t0),
        )
    print(f"TOTAL @ {time.time() - t0:.2f}s")
asyncio.run(main())