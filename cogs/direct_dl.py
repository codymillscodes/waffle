import os
import re
import urllib.parse
from discord.ext import commands
from bs4 import BeautifulSoup
from loguru import logger
from config import DL_CHANNEL, WAFFLE_EMOJI
from utils.embed import download_ready
from utils.urls import Urls
from utils.connection import Connection as Conn
from utils.db import DB


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="bandcamp",
        description="Download an album from Bandcamp. Gets uploaded to my server for downloading.",
        brief="Download ANY album from bandcamp.",
    )
    async def bandcamp(self, ctx, *, url: str):
        title = await self.get_title(url)
        for t in range(len(title)):
            title[t] = re.sub(r"[^\w\s]", "", title[t].lower())
            title[t] = re.sub(r"\s+", "-", title[t])
        os.system(
            f"sh /mnt/thumb/waffle/scripts/bandcamp.sh {url} {title[1]} {title[0]} &"
        )
        logger.info(f"Downloading {title[0]} by {title[1]}")
        await ctx.message.add_reaction(WAFFLE_EMOJI)

    @commands.command(
        name="ytmp3",
        description="At the moment, it only returns the mp3 of a youtube video.",
        brief="Get mp3 of YT video.",
    )
    async def ytmp3(self, ctx, *, input: str):
        if "youtube" in input or "youtu.be" in input:
            link = input
            async with Conn() as resp:
                result = await resp.get_json(Urls.DEBRID_UNLOCK + link)
            id = result["data"]["id"]
            filename = result["data"]["filename"]
            logger.info(f"Unlocking ({id}) : {filename}")
            stream = urllib.parse.quote(result["data"]["streams"][0]["id"])
            async with Conn() as resp:
                result = await resp.get_json(
                    f"{Urls.DEBRID_STREAMING}{id}&stream={stream}"
                )
            id = result["data"]["delayed"]
            logger.info(f"Got delayed ID: {id}")
            async with Conn() as resp:
                re = await resp.get_json(Urls.DEBRID_DELAYED + str(id))
            if re["data"]["status"] != 2:
                await DB().add_to_queue([id, filename, ctx.author.id, "link"])
                logger.info(f"{id} not ready, added to queue.")
                await ctx.send("It's not ready and there's no !stat for this.")
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
                dlchannel = await self.bot.fetch_channel(DL_CHANNEL)
                embed = download_ready(ctx.author, filename, link)
                logger.info(f"{id} ready.")
                await dlchannel.send(embed=embed)
        else:
            await ctx.reply("Only supports youtube for now.", mention_author=False)

    @commands.command(name="video")
    async def video(self, ctx, *, input: str):
        resolutions = [720, 480, 360, 240]
        allowed = ["youtube", "youtu.be", "ok.ru", "vimeo", "dailymotion"]
        # if input in allowed:
        link = input
        async with Conn() as resp:
            result = await resp.get_json(Urls.DEBRID_UNLOCK + link)
        id = result["data"]["id"]
        filename = result["data"]["filename"]
        logger.info(f"Unlocking ({id}) : {filename}")
        for stream in result["data"]["streams"]:
            logger.debug(f"Stream: {stream}")
            if stream["quality"] == 1080:
                logger.debug(stream["id"])
                stream = urllib.parse.quote(stream["id"]).replace("-", "%2D")
                break
            elif stream["quality"] in resolutions and stream != "":
                logger.debug(stream["id"])
                stream = urllib.parse.quote(stream["id"]).replace("-", "%2D")
                break
        if stream == "":
            await ctx.send("No 1080p, 720p, 480p, 360p or 240p found.")
            return
        async with Conn() as resp:
            result = await resp.get_json(f"{Urls.DEBRID_STREAMING}{id}&stream={stream}")
        logger.info(f"url: {Urls.DEBRID_STREAMING}{id}&stream={stream}")
        try:
            id = result["data"]["delayed"]
            logger.info(f"Got delayed ID: {id}")
            async with Conn() as resp:
                re = await resp.get_json(Urls.DEBRID_DELAYED + str(id))
            if re["data"]["status"] != 2:
                await DB().add_to_queue([id, filename, ctx.author.id, "link"])
                logger.info(f"{id} not ready, added to queue.")
                await ctx.send("It's not ready and there's no !stat for this.")
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
        except KeyError:
            link = result["data"]["link"]

        dlchannel = await self.bot.fetch_channel(DL_CHANNEL)
        embed = download_ready(ctx.author, filename, link)
        logger.info(f"{id} ready.")
        await dlchannel.send(embed=embed)
        # else:
        #    await ctx.reply("Only supports youtube for now.", mention_author=False)

    async def get_title(self, url):
        async with Conn() as resp:
            r = await resp.get_text(url)
        soup = BeautifulSoup(r, "html.parser")
        s = soup.find("meta", property="og:title")
        title = s["content"].split(", by ")
        logger.info(f"Got title: {title}")
        return title


async def setup(bot):
    await bot.add_cog(DirectDLCog(bot))
