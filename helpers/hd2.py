import httpx


async def helldivers_events():  # events for now
    url = "https://api.live.prod.thehelldiversgame.com/api/WarSeason/801/Status"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    events = resp.json()["globalEvents"]
    print(events)
    return events
