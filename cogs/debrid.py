import discord
from discord.ext import commands
from py1337x import py1337x
import asyncio
from loguru import logger
import config
from hurry.filesize import size
import urllib.parse
from alldebrid_api import magnet
from alldebrid_api import debrid_url
import requests
import time
import aiohttp

torrents = py1337x(proxy="1337x.to")
# torrents.search('harry potter', category='movies', sortBy='seeders', order='desc')
class DebridCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.debrid_key
        self.api_host = config.debrid_host
        self.token = ""
        self.session = aiohttp.ClientSession()

    @commands.command(name="deletetorrents")
    async def deletetorrents(self, ctx, *, input: int):
        r = requests.get(
            debrid_url.create(
                request="ready", agent=self.api_host, api_key=self.api_key
            )
        ).json()["data"]["magnets"]

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
        await ctx.send(f"{input} old torrents deleted.")

    @commands.command(name="ready")
    async def ready(self, ctx):
        r = requests.get(
            debrid_url.create(request="all", agent=self.api_host, api_key=self.api_key)
        )
        await ctx.send(
            f"{len(r.json()['data']['magnets'])} torrents.\nThe limit is 1000."
        )

    @commands.command(name="magnet")
    async def hosts(self, ctx, *, input: str):
        if input.startswith("magnet"):
            mag = magnet.upload_magnet(input, agent=self.api_host, api_key=self.api_key)
            if mag[2]:
                em_links = discord.Embed(description=f"{ctx.author.mention}")
                link = f"{config.http_url}magnets/{urllib.parse.quote(mag[1])}/"
                em_links.add_field(
                    name=f"{mag[1]}",
                    value=f"[Click this shit for files, i am very lazy.]({link})",
                )
                dl_channel = await self.bot.fetch_channel(config.dl_channel)
                await dl_channel.send(embed=em_links)
            else:
                with open("debrid.txt", "a") as f:
                    f.write(f"{mag[0]},{ctx.author.id},magnet\n")
                await ctx.send("It aint ready. Try !stat.")
        else:
            await ctx.send("Not a valid magnet link.")

    @commands.command(name="stat")
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
                except Exception as e:
                    logger.warning("Error Occured: {e}")
                    em_status.add_field(
                        name="Error", value="Error Occured.", inline=False
                    )
            await ctx.send(embed=em_status)

    @commands.command(name="clearqueue")
    async def clearqueue(self, ctx):
        with open("debrid.txt", "w"):
            pass
        logger.info("Debrid queue cleared.")
        await ctx.send("Queue cleared.")

    @commands.command(name="queue")
    async def queue(self, ctx):
        with open("debrid.txt", "r") as f:
            out = ""
            for line in f:
                out = f"{out + line}\n"
        if len(out) < 1:
            await ctx.send("Queue is empty.")
        else:
            await ctx.send(f"```{out}```")

    @commands.command(name="rarbg")
    async def rarbg(self, ctx, *, input: str):
        self.token = get_token()
        max_requests = 10
        input = input.replace(" ", "%20")
        url = f"https://torrentapi.org/pubapi_v2.php?app_id=waffle&token={self.token}&mode=search&search_string={input}&sort=seeders&format=json_extended&category=18;41;54;50;45;44;17;48;14"
        counter = 0
        while counter < max_requests:
            # async with aiohttp.ClientSession() as session:
            async with self.session.get(url) as resp:
                r = await resp.json()
                if "torrent_results" in r:
                    break
                time.sleep(0.1)
                counter = counter + 1

        if "error_code" in r:
            if r["error_code"] == 5:
                await ctx.send(
                    "Rate limited. Try again eventually.\n1 req/2s limit. Sometimes it's just tempermental."
                )
            await ctx.send("No results. :(")
        elif len(r["torrent_results"]) > 0:
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
            await ctx.send(embed=em_result)

            def check(m):
                return m.author == ctx.author and m.content.startswith("!pick")

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=120)

                pick = int(msg.content[6:]) - 1
                if int(msg.content[6:]) > len(results) or pick < 0:
                    await ctx.send("WRONG")
                else:
                    magnet_link = results[pick]["download"]
                    # add magnet, get ready, name, id
                    mag = magnet.upload_magnet(
                        magnet_link, agent=self.api_host, api_key=self.api_key
                    )
                    if mag[2]:
                        em_links = discord.Embed(description=f"{ctx.author.mention}")
                        link = f"{config.http_url}magnets/{urllib.parse.quote(mag[1])}/"
                        em_links.add_field(
                            name=f"{mag[1]}",
                            value=f"[Click this shit for files, i am very lazy.]({link})",
                        )
                        dl_channel = await self.bot.fetch_channel(config.dl_channel)
                        await dl_channel.send(embed=em_links)
                    else:
                        with open("debrid.txt", "a") as f:
                            f.write(f"{mag[0]},{ctx.author.id},magnet\n")
                        await ctx.send("It aint ready. Try !stat.")
            except asyncio.TimeoutError:
                await ctx.send("TOO SLOW")

    @commands.command(name="search")
    async def search(self, ctx, *, input: str):
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
                    name=f"{x+1}. {torrent['name']}", value=result_value, inline=False
                )
                x = x + 1
            em_result.add_field(
                name="----------------",
                value="You should pick the one with the most seeders and a reasonable filesize. Pay attention to the quality. You dont want a cam or TS.\n*!pick 1-5*",
                inline=False,
            )
            await ctx.send(embed=em_result)

            def check(m):
                return m.author == ctx.author and m.content.startswith("!pick")

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)

                pick = int(msg.content[6:]) - 1
                if int(msg.content[6:]) > 5 or pick < 0:
                    await ctx.send("WRONG")
                else:
                    magnet_link = torrents.info(torrentId=results[pick]["torrentId"])[
                        "magnetLink"
                    ]
                    # add magnet, get ready, name, id
                    mag = magnet.upload_magnet(
                        magnet_link, agent=self.api_host, api_key=self.api_key
                    )
                    if mag[2]:
                        em_links = discord.Embed(description=f"{ctx.author.mention}")
                        link = f"{config.http_url}magnets/{urllib.parse.quote(mag[1])}/"
                        em_links.add_field(
                            name=f"{mag[1]}",
                            value=f"[Click this shit for files, i am very lazy.]({link})",
                        )
                        dl_channel = await self.bot.fetch_channel(config.dl_channel)
                        await dl_channel.send(embed=em_links)
                    else:
                        with open("debrid.txt", "a") as f:
                            f.write(f"{mag[0]},{ctx.author.id},magnet\n")
                        await ctx.send("It aint ready. Try !stat.")

            except asyncio.TimeoutError:
                await ctx.send("TOO SLOW")
        else:
            await ctx.send("Zero results.")

    # @commands.command(name="bandcamp")
    # async def status(self, ctx, *, url: str):
    #     os.system(f"bandcamp-dl --base-dir=/mnt/ext/music {url}")
    #     await ctx.send("Done! [ftp link]")

    # @commands.command(name="unlock")
    # async def unlock(self, ctx, *, input: str):
    #     await ctx.send(input)


def get_token():
    try:
        r = requests.get(
            f"https://torrentapi.org/pubapi_v2.php?app_id=waffle&get_token=get_token"
        )
        return r.json()["token"]
    except IndexError:
        logger.error(f"Failed to get torrent token.\n{r.json()}")


def setup(bot):
    bot.add_cog(DebridCog(bot))


def percentage(curr, total):
    if not (isinstance(curr, (int, float)) and isinstance(total, (int, float))):
        raise ValueError("Both curr and total should be numerical values")
    if total == 0:
        raise ValueError("Total can not be zero")
    num = curr / total
    return f"{num:.2%}"
