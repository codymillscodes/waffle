import time
import random
import urllib.parse
import asyncio
import aiohttp
import requests
import discord
from discord.ext import commands
from py1337x import py1337x
from loguru import logger
from hurry.filesize import size
from alldebrid_api import magnet
from alldebrid_api import debrid_url
import config

LINK_MSG = [
    "Click this shit for files, i am very lazy.",
    "linky linky",
    "this is a link",
    "3=====D~~",
    "Follow the rabbit hole to the files",
    "File access granted, click at your own risk",
    "The files are waiting for you, just one click away",
    "Get ready for the ride, files incoming",
    "The files are calling your name, answer the call",
    "Link to enlightenment (and files)",
    "It's not just a link, it's an adventure",
    "Links, files, and good times await",
    "You can't handle the link, or can you?",
    "It's a link to remember",
    "File me away, I'm ready to be clicked",
    "Buckle up, it's a wild link ride",
]
torrents = py1337x(proxy="1337x.to")
# torrents.search('harry potter', category='movies', sortBy='seeders', order='desc')
class DebridCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.debrid_key
        self.api_host = config.debrid_host
        self.token = ""
        self.session = aiohttp.ClientSession()
        self.timeout = aiohttp.ClientTimeout(total=60)

    @commands.command(
        name="deletetorrents", description="Delete x amount of old torrents."
    )
    async def deletetorrents(self, ctx, *, input: int):
        async with self.session.get(
            debrid_url.create(
                request="ready", agent=self.api_host, api_key=self.api_key
            ),
            timeout=self.timeout,
        ) as resp:
            r = await resp.json()["data"]["magnets"]
        logger.info(f"{len(r)} torrents cached.")
        mag_slice = []
        for torrent in r:
            mag_slice.append(torrent)
        mag_slice = mag_slice[-(input):]
        ids = []
        for torrent in r:
            if torrent in mag_slice:
                ids.append(r[torrent]["id"])
        for i in ids:
            magnet.delete_magnet(i, agent=self.api_host, api_key=self.api_key)
            time.sleep(0.1)
        logger.info(f"{input} old torrents deleted.")
        await ctx.reply(f"{input} old torrents deleted.")

    @commands.command(
        name="ready", description="Returns the number of cached torrents."
    )
    async def ready(self, ctx):
        async with self.session.get(
            debrid_url.create(request="all", agent=self.api_host, api_key=self.api_key),
            timeout=self.timeout,
        ) as resp:
            r = await resp.json()["data"]["magnets"]
        logger.info(f"{len(r)} cached torrents.")
        await ctx.send(f"{len(r)} torrents.\nThe limit is 1000.")

    @commands.command(name="magnet", description="Upload a magnet directly.")
    async def mag(self, ctx, *, input: str):
        if input.startswith("magnet"):
            mag = magnet.upload_magnet(input, agent=self.api_host, api_key=self.api_key)
            logger.info(f"Adding magnet for {mag[1]}")
            if mag[2]:
                em_links = discord.Embed(description=f"{ctx.author.mention}")
                link = f"{config.http_url}magnets/{urllib.parse.quote(mag[1])}/"
                em_links.add_field(
                    name=f"{mag[1]}",
                    value=f"[{random.choice(LINK_MSG)}]({link})",
                )
                logger.info(f"{mag[1]} is ready.")
                dl_channel = await self.bot.fetch_channel(config.dl_channel)
                await dl_channel.send(embed=em_links)
            else:
                with open("debrid.txt", "a") as f:
                    f.write(f"{mag[0]},{ctx.author.id},magnet\n")
                logger.info(f"{mag[1]} is not ready. Adding to queue.")
                await ctx.reply("It aint ready. Try !stat.", mention_author=False)
        else:
            logger.info(f"Invalid link recv'd: {input}")
            await ctx.reply("Not a valid magnet link.", mention_author=False)

    @commands.command(name="stat", description="Returns status of active torrents.")
    async def stat(self, ctx):
        all_status = magnet.get_all_magnet_status(
            agent=self.api_host, api_key=self.api_key
        )
        if all_status == 0:
            await ctx.send("No active downloads.")
        else:
            if all_status:
                em_status = discord.Embed(description="Active downloads:")
                try:
                    for m in all_status:
                        name = all_status[m].get("filename", "")
                        dlsize = float(all_status[m].get("size", 0))
                        seeders = all_status[m].get("seeders", 0)
                        speed = all_status[m].get("downloadSpeed", 0)
                        complete = float(all_status[m].get("downloaded", 0))
                        sized_size = 0
                        percentage_complete = "0%"
                        if dlsize > 0:
                            sized_size = size(int(dlsize))
                        if speed > 0:
                            speed = size(int(speed))
                        if complete > 0:
                            percentage_complete = percentage(complete, dlsize)
                        em_status.add_field(
                            name=name,
                            value=f"{percentage_complete} of {sized_size} | Seeders: {seeders} | Speed: {speed}",
                            inline=False,
                        )
                except Exception as ex:
                    logger.warning("Error Occured: {ex}")
                    em_status.add_field(name="Error", value=f"{ex}", inline=False)
            await ctx.reply(embed=em_status, mention_author=False)

    @commands.command(name="clearqueue", description="Clear active torrent queue.")
    async def clearqueue(self, ctx):
        with open("debrid.txt", "w"):
            pass
        logger.info("Debrid queue cleared.")
        await ctx.send("Queue cleared.")

    @commands.command(
        name="queue", description="Returns raw output of active torrent queue."
    )
    async def queue(self, ctx):
        with open("debrid.txt", "r") as f:
            out = ""
            for line in f:
                out = f"{out + line}\n"
        logger.info(f"{len(out)} links/magnets in queue.")
        if len(out) < 1:
            await ctx.reply("Queue is empty.", mention_author=False)
        else:
            await ctx.reply(f"```{out}```", mention_author=False)

    @commands.command(
        name="search",
        aliases=["rarbg"],
        description="Search 1337x or declare an emergency by searching with !rarbg",
    )
    async def search(self, ctx, *, input: str):
        logger.info(f"{ctx.invoked_with} {input}")

        def check(m):
            return m.author == ctx.author and m.content.startswith("!pick")

        if ctx.invoked_with == "rarbg":
            self.token = get_token()
            max_requests = 10
            input = input.replace(" ", "%20")
            url = f"https://torrentapi.org/pubapi_v2.php?app_id=waffle&token={self.token}&mode=search&search_string={input}&sort=seeders&format=json_extended&category=18;41;54;50;45;44;17;48;14"
            counter = 0
            while counter < max_requests:
                async with self.session.get(url, timeout=self.timeout) as resp:
                    r = await resp.json()
                    if "torrent_results" in r:
                        break
                    time.sleep(0.1)
                    counter = counter + 1

            if "error_code" in r:
                if r["error_code"] == 5:
                    logger.info("rarbg rate-limited.")
                    await ctx.reply(
                        "Rate limited. Try again eventually.\n1 req/2s limit. Sometimes it's just tempermental.",
                        mention_author=False,
                    )
                logger.info(f"rarbg:error_code: {r['error_code']}")
                await ctx.reply("No results. :(", mention_author=False)
            elif len(r["torrent_results"]) > 0:
                logger.info(f"{len(r['torrent_results'])} torrent results.")
                if len(r["torrent_results"]) > 10:
                    results = r["torrent_results"][:10]
                else:
                    results = r["torrent_results"]
                em_result = discord.Embed(
                    description=":rotating_light::bangbang:__***YOU HAVE DECLARED A TORRENT EMERGENCY***__:bangbang::rotating_light:"
                )
                x = 0
                for m in results:
                    x = x + 1
                    result_value = f"Seeders: {m['seeders']} | Leechers: {m['leechers']} | Size: {size(int(m['size']))}"
                    em_result.add_field(
                        name=f"{x}. {m['title']}", value=result_value, inline=False
                    )

                em_result.add_field(
                    name="----------------",
                    value=f"More results, longer timeout. Don't fuck it up cause it probably won't work twice in a row!\n*!pick 1-{len(results)}*",
                    inline=False,
                )
                await ctx.reply(embed=em_result)
        else:
            results = torrents.search(input, sortBy="seeders", order="desc")
            sanitized_results = []
            for torrent in results["items"]:
                info = torrents.info(torrentId=torrent["torrentId"])
                if "xxx".upper() not in info["category"]:
                    sanitized_results.append(torrent)
                if len(sanitized_results) > 5:
                    break
            if len(sanitized_results) > 0:
                em_result = discord.Embed()
                if len(sanitized_results) > 5:
                    results = sanitized_results[:5]
                else:
                    results = sanitized_results

                x = 0
                for torrent in results:
                    result_value = f"Seeders: {torrent['seeders']} | Leechers: {torrent['leechers']} | Size: {torrent['size']}"
                    em_result.add_field(
                        name=f"{x+1}. {torrent['name']}",
                        value=result_value,
                        inline=False,
                    )
                    x = x + 1
                em_result.add_field(
                    name="----------------",
                    value="You should pick the one with the most seeders and a reasonable filesize. Pay attention to the quality. You dont want a cam or TS.\n*!pick 1-5*",
                    inline=False,
                )
                await ctx.reply(embed=em_result)

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)

                pick = int(msg.content[6:]) - 1
                if int(msg.content[6:]) > 5 or pick < 0:
                    await ctx.send("WRONG")
                else:
                    if ctx.invoked_with == "rarbg":
                        magnet_link = results[pick]["download"]
                    else:
                        magnet_link = torrents.info(
                            torrentId=results[pick]["torrentId"]
                        )["magnetLink"]
                    # add magnet, get ready, name, id
                    mag = magnet.upload_magnet(
                        magnet_link, agent=self.api_host, api_key=self.api_key
                    )
                    if mag[2]:
                        em_links = discord.Embed(description=f"{ctx.author.mention}")
                        link = f"{config.http_url}magnets/{urllib.parse.quote(mag[1])}/"
                        em_links.add_field(
                            name=f"{mag[1]}",
                            value=f"[{random.choice(LINK_MSG)}]({link})",
                        )
                        dl_channel = await self.bot.fetch_channel(config.dl_channel)
                        await dl_channel.send(embed=em_links)
                    else:
                        with open("debrid.txt", "a") as f:
                            f.write(f"{mag[0]},{ctx.author.id},magnet\n")
                        await ctx.reply(
                            "It aint ready. Try !stat.", mention_author=False
                        )

            except asyncio.TimeoutError:
                await ctx.send("TOO SLOW", mention_author=False)
            else:
                await ctx.reply("Zero results.", mention_author=False)


def get_token():
    try:
        r = requests.get(
            "https://torrentapi.org/pubapi_v2.php?app_id=waffle&get_token=get_token",
            timeout=30,
        )
        logger.info("Got token.")
        logger.debug(f"Token: {r.json()['token']}")
        return r.json()["token"]
    except IndexError:
        logger.error(f"Failed to get torrent api token.\n{r.json()}")


def setup(bot):
    bot.add_cog(DebridCog(bot))


def percentage(curr, total):
    if not (isinstance(curr, (int, float)) and isinstance(total, (int, float))):
        raise ValueError("Both curr and total should be numerical values")
    if total == 0:
        raise ValueError("Total can not be zero")
    num = curr / total
    return f"{num:.2%}"
