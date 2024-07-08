import asyncio
import time
import os

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger
import httpx
from bs4 import BeautifulSoup as bs

import config
import helpers.debrid as deb
import helpers.embed
from helpers.db import DB
import strings.urls as Urls
import helpers.yar as yar


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
    async def deletetorrents(self, ctx, *, num: int):
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.DEBRID_STATUS_READY)
            r = r.json()["data"]["magnets"]

        logger.info(f"{len(r)} torrents cached.")
        mag_slice = []
        for torrent in r:
            mag_slice.append(torrent)
        mag_slice = mag_slice[-num:]
        ids = []
        for torrent in r:
            if torrent in mag_slice:
                ids.append(r[torrent]["id"])
        for i in ids:
            await deb.delete_magnet(i)
            time.sleep(0.1)
        logger.info(f"{num} old torrents deleted.")
        await ctx.reply(f"{num} old torrents deleted.")

    @commands.command(
        name="ready",
        description="Returns the number of cached torrents.",
        brief="Returns the number of cached torrents.",
    )
    async def ready(self, ctx):
        r = await deb.get_all_magnet_status()
        logger.info(f"{len(r)} cached torrents.")
        await ctx.send(f"{len(r)} torrents.\nThe limit is 1000.")

    @app_commands.command(
        name="magnet",
        description="Upload a magnet directly.",
    )
    async def mag(self, interaction: discord.Interaction, magnet: str):
        if magnet.startswith("magnet"):
            await interaction.response.defer(thinking=True)
            mag = await deb.upload_magnet(magnet)
            logger.info(f"Adding magnet for {mag[1]}")
            if mag[2]:
                embed = helpers.embed.download_ready(interaction.user, mag[1])
                logger.info(f"{mag[1]} is ready.")
                dl_channel = await self.bot.fetch_channel(config.DL_CHANNEL)
                await dl_channel.send(embed=embed)
                await interaction.followup.send("Download ready and waiting!")
            else:
                data = [mag[0], "magnet", interaction.user.id, "magnet"]
                await DB().add_to_queue(data)
                logger.info(f"{mag[1]} is not ready. Adding to queue.")
                await interaction.followup.send("It aint ready. Try !stat.")
        else:
            logger.info(f"Invalid link recv'd: {magnet}")
            await interaction.response.send_message("Not a valid magnet link.")

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
                embed = helpers.embed.debrid_status(all_status)
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as ex:
                logger.warning(f"Error Occurred: {ex}")
                await ctx.reply("Error occurred. Try again later.")

    @app_commands.command(
        name="m3u",
        description="generate playlist of debrid links for easy streaming in vlc",
    )
    async def m3u_gen(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True)
        logger.info("Generating M3U")
        exclude_files = ["txt", "../"]
        files = []
        async with httpx.AsyncClient() as resp:
            r = await resp.get(url)
        m3u_name = f"{url.split('/')[-2]}.m3u"
        # m3u_name = m3u_name
        soup = bs(r, "html.parser")
        for tag in soup.find_all("a"):
            if (
                tag.get("href")[-3:] in exclude_files
                or tag.get("href") in exclude_files
            ):
                continue

            files.append(f"{url}{tag.get('href')}\n")

        logger.info(f"M3U List: {files}")
        logger.info(f"File name: {m3u_name}")
        with open(f"tmp/{m3u_name}", "a") as f:
            for file in files:
                f.write(file)
        await interaction.followup.send(file=discord.File(f"tmp/{m3u_name}"))
        os.remove(f"tmp/{m3u_name}")
        logger.info("Sent and removed M3U.")

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

    @commands.command(name="fg", aliases=["search"], description="searchin")
    async def fg(self, ctx, *, query: str):
        logger.info(f"{ctx.invoked_with} {query}")

        results = await yar.search_jackett(query)
        if len(results) == 0:
            await ctx.reply("No results. :(", mention_author=False)
        else:
            embed = helpers.embed.torrent_results(results)
            e = await ctx.reply(embed=embed, mention_author=False)

            def check(m):
                return m.author == ctx.author and m.content.startswith(
                    ("!pick", "!Pick", "!search")
                )

            try:
                not_ready = 0
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                if not msg.content.startswith(("!pick", "!Pick")):
                    # await ctx.invoke(self.search, input=msg.content[8:])
                    await e.add_reaction("❌")
                elif msg.content.startswith("!pick"):
                    pick = deb.eval_pick(msg.content.replace("!pick", "").strip())
                    pick = int(msg.content[6:]) - 1
                    if pick > 10:
                        await ctx.send("WRONG")
                    elif pick < 0:
                        await e.add_reaction("❌")
                    else:
                        dl_channel = await self.bot.fetch_channel(config.DL_CHANNEL)
                        picked_torrent = list(results)[pick]
                        if picked_torrent["indexer"] == "TheRARBG":
                            logger.info(picked_torrent["url"])
                            magnet_link = await yar.rarbg(picked_torrent["url"])
                        else:
                            magnet_link = picked_torrent["magnet"]

                        mag = await deb.upload_magnet(magnet_link)
                        if mag[2]:
                            embed = helpers.embed.download_ready(ctx.author.id, mag[1])
                            await dl_channel.send(embed=embed)
                        else:
                            await DB().add_to_queue(
                                [mag[0], query, ctx.author.id, "magnet"]
                            )
                            not_ready += 1
                    if not_ready == 0:
                        await ctx.reply(
                            f"Sent download to <#{config.DL_CHANNEL}>",
                            mention_author=False,
                        )
                    else:
                        await ctx.reply(
                            f"Not ready. Added to queue.",
                            mention_author=False,
                        )
            except asyncio.TimeoutError:
                # await ctx.send("TOO SLOW", mention_author=False)
                # add reaction to previously sent em_result embed
                await e.add_reaction("❌")
                # await ctx.send("something broke lol")
            except Exception as e:
                logger.exception(e)
                await ctx.reply(f"EXCEPTION!\n {type(e).__name__}")


async def setup(bot):
    await bot.add_cog(DebridCog(bot))
