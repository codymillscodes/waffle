import time
import random
import urllib.parse
import asyncio
import discord
from discord.ext import commands
from py1337x import py1337x
from loguru import logger
from hurry.filesize import size
import utils.debrid_urls as debrid_url
import utils.embed
import config

torrents = py1337x(proxy="1337x.to")
# torrents.search('harry potter', category='movies', sortBy='seeders', order='desc')
class DebridCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.debrid_key
        self.api_host = config.debrid_host
        self.token = ""

    @commands.command(
        name="deletetorrents",
        description="Delete x amount of old torrents.",
        brief="Delete x amount of old torrents.",
    )
    async def deletetorrents(self, ctx, *, input: int):
        async with self.bot.session.get(
            debrid_url.create(
                request="ready", agent=self.api_host, api_key=self.api_key
            ),
            timeout=self.bot.timeout,
        ) as resp:
            r = await resp.json()
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
            await debrid_url.delete_magnet(
                i, agent=self.api_host, api_key=self.api_key, bot=self.bot
            )
            time.sleep(0.1)
        logger.info(f"{input} old torrents deleted.")
        await ctx.reply(f"{input} old torrents deleted.")

    @commands.command(
        name="ready",
        description="Returns the number of cached torrents.",
        brief="Returns the number of cached torrents.",
    )
    async def ready(self, ctx):
        async with self.bot.session.get(
            debrid_url.create(request="all", agent=self.api_host, api_key=self.api_key),
            timeout=self.bot.timeout,
        ) as resp:
            r = await resp.json()
            r = r["data"]["magnets"]
        logger.info(f"{len(r)} cached torrents.")
        await ctx.send(f"{len(r)} torrents.\nThe limit is 1000.")

    @commands.command(
        name="magnet",
        description="Upload a magnet directly.",
        brief="Upload a magnet directly.",
    )
    async def mag(self, ctx, *, input: str):
        if input.startswith("magnet"):
            mag = await debrid_url.upload_magnet(
                input, agent=self.api_host, api_key=self.api_key, bot=self.bot
            )
            logger.info(f"Adding magnet for {mag[1]}")
            if mag[2]:
                embed = utils.embed.download_ready(ctx.author, mag)
                logger.info(f"{mag[1]} is ready.")
                dl_channel = await self.bot.fetch_channel(config.dl_channel)
                await dl_channel.send(embed=embed)
            else:
                with open("debrid.txt", "a") as f:
                    f.write(f"{mag[0]},{ctx.author.id},magnet\n")
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
        all_status = await debrid_url.get_all_magnet_status(
            agent=self.api_host, api_key=self.api_key, bot=self.bot
        )
        if all_status == 0:
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
        with open("debrid.txt", "w"):
            pass
        logger.info("Debrid queue cleared.")
        await ctx.send("Queue cleared.")

    @commands.command(
        name="queue",
        description="Returns raw output of active torrent queue.",
        brief="Returns raw output of active torrent queue.",
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

        if ctx.invoked_with == "rarbg":
            self.token = self.get_token()
            max_requests = 10
            input = input.replace(" ", "%20")
            url = f"https://torrentapi.org/pubapi_v2.php?app_id=waffle&token={self.token}&mode=search&search_string={input}&sort=seeders&format=json_extended&category=18;41;54;50;45;44;17;48;14"
            counter = 0
            while counter < max_requests:
                async with self.bot.session.get(url, timeout=self.bot.timeout) as resp:
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
                    mag = await debrid_url.upload_magnet(
                        magnet_link,
                        agent=self.api_host,
                        api_key=self.api_key,
                        bot=self.bot,
                    )
                    if mag[2]:
                        embed = utils.embed.download_ready(ctx.author, mag)
                        dl_channel = await self.bot.fetch_channel(config.dl_channel)
                        await dl_channel.send(embed=embed)
                    else:
                        with open("debrid.txt", "a") as f:
                            f.write(f"{mag[0]},{ctx.author.id},magnet\n")
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
            async with self.bot.session.get(
                "https://torrentapi.org/pubapi_v2.php?app_id=waffle&get_token=get_token",
                timeout=30,
            ) as resp:
                r = await resp.json()
            logger.info("Got token.")
            logger.debug(f"Token: {r.json()['token']}")
            return r.json()["token"]
        except IndexError:
            logger.error(f"Failed to get torrent api token.\n{r.json()}")


def setup(bot):
    bot.add_cog(DebridCog(bot))
