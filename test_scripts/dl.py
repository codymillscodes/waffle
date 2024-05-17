import httpx
from bs4 import BeautifulSoup as bs

url = "http://192.168.1.238:9117/api/v2.0/indexers/all/results/torznab/api?apikey=p7nkqu9nxuc1nz6odzh0obf69fjoogb0&t=search&cat=2000,3000,4000,5000,7000,&q=dragon+ball"
timeout_settings = httpx.Timeout(60.0)
r = httpx.get(url, timeout=timeout_settings)
# soup = bs(r.text, features="xml")
# seeders = soup.find_all("torznab:attr", attrs={"name": "seeders"})
# for s in seeders:
#     print(s)


def sort_and_filter_xml(xml_data):
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


def rarbg(url):
    # async with httpx.AsyncClient() as client:
    response = httpx.get(url)

    tpage = bs(response.text, features="html.parser")
    magnet_link = tpage.select_one("a[href*=magnet]")
    return magnet_link["href"]


# def ebookbay():
#     pass
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# Example usage:
sorted_filtered_items = sort_and_filter_xml(r.text)[:10]
filtered_slice = sorted_filtered_items[:10]
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
            url = s.find("guid").text
            magnet = rarbg(url)
    torrent = {
        "name": title,
        "seeders": seeders,
        "indexer": indexer,
        "magnet": magnet,
        "size": sizeof_fmt(int(size)),
    }
    results.append(torrent)

print(results)
