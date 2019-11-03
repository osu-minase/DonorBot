import asyncio
import globals
def sync_corotine(coro):
    fut = asyncio.run_coroutine_threadsafe(coro, globals.client.loop)
    try:
        fut.result()
    except (asyncio.CancelledError, asyncio.TimeoutError):
        pass
    return