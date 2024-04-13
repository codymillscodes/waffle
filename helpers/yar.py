from bs4 import BeautifulSoup as bs
import httpx
from config import JACKETT_URL
from helpers.utils import sizeof_fmt


async def sort_and_filter_xml(xml_data):
    soup = bs(xml_data, "xml")
    items = soup.find_all("item")

    # Filter out items with seeders=0
    filtered_items = [
        item
        for item in items
        if item.find("torznab:attr", attrs={"name": "seeders", "value": "0"}) is None
    ]

    # Sort items by seeders (ascending order)
    sorted_items = sorted(
        filtered_items,
        key=lambda x: int(x.find("torznab:attr", attrs={"name": "seeders"})["value"]),
        reverse=True,
    )

    return sorted_items


async def rarbg(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    tpage = bs(response.text, features="html.parser")
    magnet_link = tpage.select_one("a[href*=magnet]")
    return magnet_link["href"]


async def search_jackett(query):
    url = f"{JACKETT_URL}{query.replace(' ', '+')}"
    timeout_settings = httpx.Timeout(60.0)
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=timeout_settings)
    sorted_filtered_items = await sort_and_filter_xml(r.text)
    sorted_filtered_items = sorted_filtered_items[:10]
    results = []
    for s in sorted_filtered_items:
        title = s.find("title").text
        seeders = s.find("torznab:attr", attrs={"name": "seeders"})["value"]
        indexer = s.find("jackettindexer").text
        size = s.find("size").text
        url = s.find("guid").text
        try:
            magnet = s.find("torznab:attr", attrs={"name": "magneturl"})["value"]
        except:
            if "TheRARBG" in indexer:
                magnet = "None"
        torrent = {
            "name": title,
            "seeders": seeders,
            "indexer": indexer,
            "url": url,
            "magnet": magnet,
            "size": sizeof_fmt(int(size)),
        }
        results.append(torrent)

    return results
