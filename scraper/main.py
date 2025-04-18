import asyncio
from collections import defaultdict
import httpx
import time
from common.db import provision_database_schema, data_exists
from common.logger import logger
from car_data_persister import CarDataPersister
from scraper import CarDataScraper

async def main():
    logger.info("Scraper is Ready")
    await provision_database_schema()
    if await data_exists():
        logger.info("Our database already has the data we need. No need to scrape")
        return
    limits = httpx.Limits(
        max_connections=1
    )
    async with httpx.AsyncClient(limits=limits) as client:
        scraper = CarDataScraper(client)
        start = time.perf_counter()

        makes = await scraper.get_makes()

        # asyncio.gather helps us maximize speed
        model_tasks = {
            make_name: scraper.get_models(make_url)
            for make_name, make_url in makes
        }
        models_for_make_results = await asyncio.gather(*model_tasks.values())
        models_for_make = dict(zip(model_tasks.keys(), models_for_make_results))

        parts_tasks = []
        for make, models in models_for_make.items():
            for model_name, model_url in models:
                parts_tasks.append((make, model_name, scraper.get_parts(model_url)))

        results = await asyncio.gather(*(t[2] for t in parts_tasks))

        end = time.perf_counter()
        elapsed = end - start
        logger.info(f"📊 Scraping + saving completed in {elapsed:.2f} seconds")

        all_parts = defaultdict(dict)
        for (make, model_name, _), parts in zip(parts_tasks, results):
            all_parts[make][model_name] = parts

        persister = CarDataPersister()
        logger.info("Saving to DB...")
        await persister.save(all_parts)


if __name__ == "__main__":
    asyncio.run(main())
