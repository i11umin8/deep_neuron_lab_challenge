from bs4 import BeautifulSoup
import httpx
from common.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
BASE_URL = "https://www.urparts.com/"
CATALOGUE_URL = f"{BASE_URL}index.cfm/page/catalogue"


class CarDataScraper:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=False
    )
    async def fetch_html(self, url: str) -> BeautifulSoup | None:
        try:
            response = await self.client.get(url, timeout=10.0)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_link(self, link):
        name = link.text.strip()
        href = link["href"]
        return name, BASE_URL.rstrip("/") + "/" + href.lstrip("/")

    async def get_makes(self):
        soup = await self.fetch_html(CATALOGUE_URL)
        makes = []
        if not soup:
            return makes
        container = soup.find("div", class_="c_container allmakes")
        if not container:
            logger.warning("No makes container found!")
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

