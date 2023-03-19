import time
import asyncio
from discord.ext import commands
from py1337x import py1337x
from loguru import logger
import utils.debrid as deb
import utils.embed
from utils.urls import Urls
import config
from utils.connection import Connection as Conn
from utils.db import DB

torrents = py1337x(proxy="1337x.to")
# torrents.search('harry potter', category='movies', sortBy='seeders', order='desc')
class DebridCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.DEBRID_KEY
        self.api_host = config.DEBRID_AGENT
        self.token = ""

    @commands.command(
        name="deletetorrents",
        description="Delete x amount of old torrents.",
        brief="Delete x amount of old torrents.",
    )
    async def deletetorrents(self, ctx, *, input: int):
        async with Conn() as resp:
            r = await resp.get_json(Urls.DEBRID_STATUS_READY)
            r = r["data"]["magnets"]

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
            await deb.delete_magnet(i)
            time.sleep(0.1)
        logger.info(f"{input} old torrents deleted.")
        await ctx.reply(f"{input} old torrents deleted.")

    @commands.command(
        name="ready",
        description="Returns the number of cached torrents.",
        brief="Returns the number of cached torrents.",
    )
    async def ready(self, ctx):
        r = await deb.get_all_magnet_status()
        logger.info(f"{len(r)} cached torrents.")
        await ctx.send(f"{len(r)} torrents.\nThe limit is 1000.")

    @commands.command(
        name="magnet",
        description="Upload a magnet directly.",
        brief="Upload a magnet directly.",
    )
    async def mag(self, ctx, *, input: str):
        if input.startswith("magnet"):
            mag = await deb.upload_magnet(input)
            logger.info(f"Adding magnet for {mag[1]}")
            if mag[2]:
                embed = utils.embed.download_ready(ctx.author, mag)
                logger.info(f"{mag[1]} is ready.")
                dl_channel = await self.bot.fetch_channel(config.DL_CHANNEL)
                await dl_channel.send(embed=embed)
            else:
                data = [mag[0], "magnet", ctx.author.id, "magnet"]
                await DB().add_to_queue(data)
                logger.info(f"{mag[1]} is not ready. Adding to queue.")
                await ctx.reply("It aint ready. Try !stat.", mention_author=False)
        else:
            logger.info(f"Invalid link recv'd: {input}")
            await ctx.reply("Not a valid magnet link.", mention_author=False)

    @commands.command(
        name="stat",
        description="Returns status of active torrents.",
        brief="Returns status of active torrents.",
    )
    async def stat(self, ctx):
        all_status = await deb.get_active_magnets()
        if len(all_status) <= 0:
            await ctx.send("No active downloads.")
        else:
            try:
                embed = utils.embed.debrid_status(all_status)
            except Exception as ex:
                logger.warning(f"Error Occured: {ex}")
                await ctx.reply("Error occured. Try again later.")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        name="clearqueue",
        description="Clear active torrent queue.",
        brief="Clear active torrent queue.",
    )
    async def clearqueue(self, ctx):
        queue = await DB().get_active_queue()
        for q in queue:
            await DB().set_status(task_id=q["task_id"], status="cancelled")
        logger.info("Debrid queue cleared.")
        await ctx.send("Queue cleared.")

    @commands.command(
        name="queue",
        description="Returns raw output of active torrent queue.",
        brief="Returns raw output of active torrent queue.",
    )
    async def queue(self, ctx):
        queue = await DB().get_active_queue()
        queue = list(queue)
        logger.info(f"{len(queue)} links/magnets in queue.")
        if len(queue) < 1:
            await ctx.reply("Queue is empty.", mention_author=False)
        else:
            await ctx.reply(
                "```{}```".format("\n".join([str(i["task_name"]) for i in queue])),
                mention_author=False,
            )

    @commands.command(
        name="search",
        aliases=["rarbg"],
        description="Search 1337x or declare an emergency by searching with !rarbg",
    )
    async def search(self, ctx, *, input: str):
        logger.info(f"{ctx.invoked_with} {input}")

        if ctx.invoked_with == "rarbg":
            self.token = self.get_token()
            max_requests = 10
            input = input.replace(" ", "%20")
            url = f"{Urls.RARBG_API}{self.token}&search_string={input}"
            counter = 0
            while counter < max_requests:
                async with Conn() as resp:
                    r = await resp.get_json(url)
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
                embed = utils.embed.torrent_results(r, emergency=True)
                e = await ctx.reply(embed=embed, mention_author=False)
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
                embed = utils.embed.torrent_results(sanitized_results)
                e = await ctx.reply(embed=embed, mention_author=False)
            else:
                await ctx.reply("Zero results.", mention_author=False)

            def check(m):
                return m.author == ctx.author and m.content.startswith("!pick")

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)

                pick = int(msg.content[6:]) - 1
                if int(msg.content[6:]) > 5:
                    await ctx.send("WRONG")
                if pick < 0:
                    await ctx.send("Godspeed.")
                else:
                    if ctx.invoked_with == "rarbg":
                        magnet_link = results[pick]["download"]
                    else:
                        # logger.info(f"results: {results}")
                        magnet_link = torrents.info(
                            torrentId=results["items"][pick]["torrentId"]
                        )["magnetLink"]
                    # add magnet, get ready, name, id
                    mag = await deb.upload_magnet(magnet_link)
                    if mag[2]:
                        embed = utils.embed.download_ready(ctx.author, mag[1])
                        dl_channel = await self.bot.fetch_channel(config.DL_CHANNEL)
                        await dl_channel.send(embed=embed)
                    else:
                        await DB().add_to_queue(
                            [mag[0], input, ctx.author.id, "magnet"]
                        )
                        await ctx.reply(
                            "It aint ready. Try !stat.", mention_author=False
                        )

            except asyncio.TimeoutError:
                # await ctx.send("TOO SLOW", mention_author=False)
                # add reaction to previously sent em_result embed
                await e.add_reaction("❌")
                # await ctx.message.add_reaction("❌")

    async def get_token(self):
        try:
            async with Conn() as resp:
                r = await resp.get_json(Urls.TOKEN_URL)
            logger.info("Got token.")
            logger.debug(f"Token: {r.json()['token']}")
            return r.json()["token"]
        except IndexError:
            logger.error(f"Failed to get torrent api token.\n{r.json()}")


async def setup(bot):
    await bot.add_cog(DebridCog(bot))
