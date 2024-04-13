<<<<<<< HEAD:helpers/yar.py
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
=======
from bs4 import BeautifulSoup as bs
import requests
import httpx
from config import JACKETT_URL


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


async def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


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
        try:
            magnet = s.find("torznab:attr", attrs={"name": "magneturl"})["value"]
        except:
            if "TheRARBG" in indexer:
                url = s.find("guid").text.replace("?format=json", "")
                magnet = await rarbg(url)
        torrent = {
            "name": title,
            "seeders": seeders,
            "indexer": indexer,
            "magnet": magnet,
            "size": await sizeof_fmt(int(size)),
        }
        results.append(torrent)

    return results


async def search_fitgirl(query):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://fitgirl-repacks.site/?s=" + query)

        if (
            "Sorry, but nothing matched your search terms. Please try again with some different keywords."
            in response.text
        ):
            return {"status": "Error", "message": "No results found."}
        fg_page = bs(response.text, features="html.parser")
        articles = fg_page.find_all("div", class_="entry-summary")
        links = {"status": "Success", "results": []}
        for a in articles:
            links["results"].append({"name": a.a.span.string, "url": a.a["href"]})

        return links
    except Exception as e:
        return {"status": "Error", "message": str(e)}


async def magnet_fitgirl(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    game_page = bs(response.text, features="html.parser")
    magnet_link = game_page.select_one("a[href*=magnet]")
    return magnet_link["href"]


# async def main():
#     try:
#         results = await search_tgx("jackass 4")
#         print(results)
#     except Exception as e:
#         print(e, results)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
>>>>>>> waffle/master:utils/yar.py
