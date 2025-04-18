import asyncio
from contextlib import asynccontextmanager

from common.db import data_exists
from typing import TYPE_CHECKING

@asynccontextmanager
async def lifespan(app: "FastAPI"):
    max_retries = 30
    delay = 2
    for attempt in range(max_retries):
        if await data_exists():
            print("✅ The data exists! 🚀🚀🚀")
            break
        print(f"Waiting for data... attempt {attempt + 1}/{max_retries}")
        await asyncio.sleep(delay)
    else:
        raise RuntimeError("Data did not become available in time. Failing startup.")
    print("API is up 🚀🚀🚀")
    yield
    # Optional: teardown logic goes here
    print("👋 App shutting down.")
