import asyncio
from contextlib import asynccontextmanager

from common.db import data_exists
from common.logger import logger
@asynccontextmanager
async def lifespan(app: "FastAPI"):
    max_retries = 30
    delay = 2
    yield
    for attempt in range(max_retries):
        if await data_exists():
            logger.info("✅ The data exists! 🚀🚀🚀")
            break
        logger.info(f"Waiting for data... attempt {attempt + 1}/{max_retries}")
        await asyncio.sleep(delay)
    else:
        logger.error("Data did not become available in time. Failing startup.")
        raise RuntimeError()
    logger.info("API is up 🚀🚀🚀")
    yield
    # Optional: teardown logic goes here
    logger.info("👋 App shutting down.")
