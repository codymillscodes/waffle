from bs4 import BeautifulSoup as bs
import requests
import httpx


async def search_tgx(query):
    query = query.replace(" ", "+")
    url = (
        f"https://torrentgalaxy.to/torrents.php?search={query}&sort=seeders&order=desc"
    )
    timeout_settings = httpx.Timeout(connect=20.0, read=40.0)
    headers = {
        "User-Agent": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"'
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, timeout=timeout_settings)
    print(resp.status_code)
    soup = bs(resp.text, features="html.parser")
    if "TGx:GalaxyFence" not in soup.title.name:
        row = soup.find_all("div", class_="tgxtablerow txlight")
        torrents = {"status": "Success", "results": []}
        # print(row)
        # window title: TGx:GalaxyFence
        for t in row:
            # print(t, "\n")
            soup = bs(str(t), features="html.parser")
            cells = soup.find_all("div", class_="tgxtablecell")
            try:
                if len(torrents["results"]) > 9:
                    break
                name = cells[3].span.b.string
                url = cells[4].select_one("a[href*=magnet]")["href"]
                size = cells[7].span.string
                seeders = cells[10].span.font.string
                leechers = cells[10].span.font.next_sibling.next_sibling.string
                # print(name.a.string, '\n', url['href'], '\n', size.string, '\n')
                torrent = {
                    "name": name,
                    "url": url,
                    "size": size,
                    "seeders": seeders,
                    "leechers": leechers,
                }
                torrents["results"].append(torrent)
            except:
                continue
        return torrents

    return {"status": "Error", "message": "captcha", "soup": soup}


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
