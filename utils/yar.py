from bs4 import BeautifulSoup as bs
import requests
import httpx


async def search_rarbg(query):
    url = f"https://therarbg.to/get-posts/keywords:{query}:ncategory:XXX/"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    soup = bs(resp.text, features="html.parser")
    # print(soup.prettify())
    tbody = soup.find("tbody")
    # torr = tbody.find_all('div')
    # print(tbody)
    torrents = {"status": "Success", "results": []}
    for t in tbody:
        soup = bs(str(t), features="html.parser")
        try:
            if len(torrents["results"]) > 9:
                break
            name = soup.find("td", class_="cellName")
            url = name.a
            size = soup.find("td", class_="sizeCell")

            # print(name.a.string, '\n', url['href'], '\n', size.string, '\n')
            torrent = {"name": name.a.string, "url": url["href"], "size": size.string}
            torrents["results"].append(torrent)
        except:
            continue
    return torrents


async def magnet_rarbg(url):
    url = f"https://therarbg.com{url}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    tpage = bs(response.text, features="html.parser")
    magnet_link = tpage.select_one("a[href*=magnet]")
    return magnet_link["href"]


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
