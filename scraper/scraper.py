# import asyncio
# import httpx
# from bs4 import BeautifulSoup
# from collections import defaultdict
# from common.models import Make, Model, Part
# from common.db import AsyncSessionLocal, init_db, data_exists
# BASE_URL = "https://www.urparts.com/"
# CATALOGUE_URL = f"{BASE_URL}index.cfm/page/catalogue"

# def extract_link(link):
#     name = link.text.strip()
#     href = link['href']
#     full_url = BASE_URL + href
#     return (name, full_url)

# async def fetch_html(client, url):
#     try:
#         response = await client.get(url, timeout=10.0)
#         response.raise_for_status()
#         return BeautifulSoup(response.text, 'html.parser')
#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# async def get_makes(client):
#     soup = await fetch_html(client, CATALOGUE_URL)
#     makes = []
#     if not soup:
#         return makes
#     container = soup.find('div', class_='c_container allmakes')
#     if not container:
#         print("No makes container found!")
#         return makes

#     for li in container.find_all('li'):
#         link = li.find('a')
#         if link:
#             makes.append(extract_link(link))
#     return makes

# async def get_models_for_make(client, make_url):
#     soup = await fetch_html(client, make_url)
#     models = []
#     if not soup:
#         return models
#     container = soup.find('div', class_='c_container allmakes allcategories')
#     if not container:
#         return models
#     for li in container.find_all('li'):
#         link = li.find('a')
#         if link:
#             models.append(extract_link(link))
#     return models

# async def get_parts_for_model(client, model_url):
#     soup = await fetch_html(client, model_url)
#     parts = []
#     if not soup:
#         return parts
#     container = soup.find('div', class_='c_container allmodels')
#     if not container:
#         return parts
#     for li in container.find_all('li'):
#         link = li.find('a')
#         if link:
#             parts.append(link.text.strip())
#     return parts

# async def save_to_db(data):
#     # await init_db()
#     async with AsyncSessionLocal() as session:
#         for make_name, models in data.items():
#             make = Make(name=make_name)
#             session.add(make)
#             await session.flush()  # get make.id

#             for model_name, parts in models.items():
#                 model = Model(name=model_name, make_id=make.id)
#                 session.add(model)
#                 await session.flush()  # get model.id

#                 for part_name in parts:
#                     part = Part(name=part_name, model_id=model.id)
#                     session.add(part)

#         await session.commit()

# async def main():
#     async with httpx.AsyncClient() as client:
#         await(init_db())
#         if await data_exists(Make):
#             print("Data exists. Exiting")
#             return
#         makes = await get_makes(client)

#         models_tasks = {
#             make_name: asyncio.create_task(get_models_for_make(client, make_url))
#             for make_name, make_url in makes
#         }
#         models_for_make = {make: await task for make, task in models_tasks.items()}

#         parts_tasks = []
#         for make, models in models_for_make.items():
#             for model_name, model_url in models:
#                 parts_tasks.append((make, model_name, model_url, asyncio.create_task(get_parts_for_model(client, model_url))))

#         all_parts = defaultdict(dict)
#         for make, model_name, _, task in parts_tasks:
#             all_parts[make][model_name] = await task

#         # Debug output (only one make/model/parts combo)
#         for make in all_parts:
#             print(f"Make: {make}")
#             for model in all_parts[make]:
#                 print(f"Model: {model}")
#                 for part in all_parts[make][model]:
#                     print(part)
#                 break
#             break
#         print("saving")
#         await save_to_db(all_parts)

# if __name__ == "__main__":
#     print("persisting the data..")
#     asyncio.run(main())


import asyncio
from collections import defaultdict
from bs4 import BeautifulSoup
import httpx

from common.models import CarMake, CarModel, CarPart
from common.db import AsyncSessionLocal, init_db, data_exists

BASE_URL = "https://www.urparts.com/"
CATALOGUE_URL = f"{BASE_URL}index.cfm/page/catalogue"


class Scraper:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch_html(self, url: str) -> BeautifulSoup | None:
        try:
            response = await self.client.get(url, timeout=10.0)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_link(self, link):
        name = link.text.strip()
        href = link["href"]
        return name, BASE_URL + href

    async def get_makes(self):
        soup = await self.fetch_html(CATALOGUE_URL)
        makes = []
        if not soup:
            return makes
        container = soup.find("div", class_="c_container allmakes")
        if not container:
            print("No makes container found!")
            return makes

        for li in container.find_all("li"):
            link = li.find("a")
            if link:
                makes.append(self.extract_link(link))
        return makes

    async def get_models(self, make_url: str):
        soup = await self.fetch_html(make_url)
        models = []
        if not soup:
            return models
        container = soup.find("div", class_="c_container allmakes allcategories")
        if not container:
            return models

        for li in container.find_all("li"):
            link = li.find("a")
            if link:
                models.append(self.extract_link(link))
        return models

    async def get_parts(self, model_url: str):
        soup = await self.fetch_html(model_url)
        parts = []
        if not soup:
            return parts
        container = soup.find("div", class_="c_container allmodels")
        if not container:
            return parts

        for li in container.find_all("li"):
            link = li.find("a")
            if link:
                parts.append(link.text.strip())
        return parts


class DataPersister:
    async def save(self, data: dict[str, dict[str, list[str]]]):
        async with AsyncSessionLocal() as session:
            for make_name, models in data.items():
                make = CarMake(name=make_name)
                session.add(make)
                await session.flush()

                for model_name, parts in models.items():
                    model = CarModel(name=model_name, make_id=make.id)
                    session.add(model)
                    await session.flush()

                    for part_name in parts:
                        part = CarPart(name=part_name, model_id=model.id)
                        session.add(part)

            await session.commit()


async def main():
    print("Initialization")
    await init_db()
    if await data_exists():
        print("Data exists. Exiting.")
        return

    async with httpx.AsyncClient() as client:
        scraper = Scraper(client)
        persister = DataPersister()

        makes = await scraper.get_makes()
        models_tasks = {
            make_name: asyncio.create_task(scraper.get_models(make_url))
            for make_name, make_url in makes
        }
        models_for_make = {make: await task for make, task in models_tasks.items()}

        parts_tasks = []
        for make, models in models_for_make.items():
            for model_name, model_url in models:
                task = asyncio.create_task(scraper.get_parts(model_url))
                parts_tasks.append((make, model_name, task))

        all_parts = defaultdict(dict)
        for make, model_name, task in parts_tasks:
            parts = await task
            all_parts[make][model_name] = parts

        # Debug preview (limit to first make/model)
        for make in all_parts:
            print(f"Make: {make}")
            for model in all_parts[make]:
                print(f"Model: {model}")
                for part in all_parts[make][model]:
                    print(part)
                break
            break

        print("Saving to DB...")
        await persister.save(all_parts)


if __name__ == "__main__":
    print("Starting data persistence...")
    asyncio.run(main())
