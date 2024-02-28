from bs4 import BeautifulSoup as bs
import requests
import httpx


async def search_tgx(query):
    query = query.replace(" ", "+")
    url = (
        f"https://torrentgalaxy.to/torrents.php?search={query}&sort=seeders&order=desc"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    soup = bs(resp.text, features="html.parser")
    row = soup.find_all("div", class_="tgxtablerow txlight")
    torrents = {"status": "Success", "results": []}
    print(row)
    # window title: TGx:GalaxyFence
    for t in row:
        print(t, "\n")
        soup = bs(str(t), features="html.parser")
        cells = soup.find_all("div", class_="tgxtablecell")
        try:
            if len(torrents["results"]) > 9:
                break
            name = cells[3]
            url = cells[4]
            size = cells[7]
            ratio = cells[10]

            # print(name.a.string, '\n', url['href'], '\n', size.string, '\n')
            torrent = {"name": name.a.string, "url": url["href"], "size": size.string}
            torrents["results"].append(torrent)
        except:
            continue
    return torrents


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


async def main():
    print(await search_tgx("jackass 4"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
