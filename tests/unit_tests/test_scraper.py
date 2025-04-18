import pytest
from bs4 import BeautifulSoup
from unittest.mock import AsyncMock, patch

# 👇 Replace with your actual module path
from scraper.scraper import CarDataScraper, BASE_URL


@pytest.mark.asyncio
async def test_extract_link():
    html = '<a href="/make1">  Make One  </a>'
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("a")
    scraper = CarDataScraper(client=None)  # no HTTP needed

    name, url = scraper.extract_link(link)
    assert name == "Make One"
    assert url == BASE_URL + "make1"


@pytest.mark.asyncio
async def test_get_makes_parses_correctly():
    html = '''
    <div class="c_container allmakes">
        <li><a href="/make1">Make One</a></li>
        <li><a href="/make2">Make Two</a></li>
    </div>
    '''
    scraper = CarDataScraper(client=AsyncMock())
    soup = BeautifulSoup(html, "html.parser")

    with patch.object(scraper, 'fetch_html', return_value=soup):
        makes = await scraper.get_makes()

    assert makes == [
        ("Make One", BASE_URL + "make1"),
        ("Make Two", BASE_URL + "make2"),
    ]


@pytest.mark.asyncio
async def test_get_models_handles_empty_container():
    html = '<div class="wrong_class"></div>'
    scraper = CarDataScraper(client=AsyncMock())
    with patch.object(scraper, 'fetch_html', return_value=BeautifulSoup(html, "html.parser")):
        models = await scraper.get_models("fake_url")
    assert models == []


@pytest.mark.asyncio
async def test_get_parts_parses_part_names():
    html = '''
    <div class="c_container allmodels">
        <li><a href="/p1">Part A</a></li>
        <li><a href="/p2">Part B</a></li>
    </div>
    '''
    scraper = CarDataScraper(client=AsyncMock())
    with patch.object(scraper, 'fetch_html', return_value=BeautifulSoup(html, "html.parser")):
        parts = await scraper.get_parts("fake_url")
    assert parts == ["Part A", "Part B"]
