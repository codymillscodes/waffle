import httpx
import json


async def helldivers_events():  # events for now
    url = "https://api.live.prod.thehelldiversgame.com/api/WarSeason/801/Status"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    events = resp.json()["globalEvents"]
    print(events)
    return events


# async def main():
#     events = await helldivers_events()
#     for e in events:
#         print(e["title"])
#         print(e["message"])


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
