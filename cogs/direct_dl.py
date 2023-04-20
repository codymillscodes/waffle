import os
import re
import urllib.parse
from discord.ext import commands
from discord import app_commands
import discord
from bs4 import BeautifulSoup
from loguru import logger
from config import DL_CHANNEL, WAFFLE_EMOJI
from utils.embed import download_ready
from utils.urls import Urls
from utils.connection import Connection as Conn
from utils.db import DB
from utils.debrid import get_tiktok_link, download_tiktok_video, delete_file


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="bandcamp",
        description="Download an album from Bandcamp. Gets uploaded to my server for downloading.",
    )
    async def bandcamp(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True)
        title = await self.get_title(url)
        for t in range(len(title)):
            title[t] = re.sub(r"[^\w\s]", "", title[t].lower())
            title[t] = re.sub(r"\s+", "-", title[t])
        os.system(
            f"sh /mnt/thumb/waffle/scripts/bandcamp.sh {url} {title[1]} {title[0]} &"
        )
        logger.info(f"Downloading {title[0]} by {title[1]}")
        await interaction.followup.send("Downloading...")

    @app_commands.command(
        name="ytmp3",
        description="At the moment, it only returns the mp3 of a youtube video.",
    )
    async def ytmp3(self, interaction: discord.Interaction, link: str):
        if "youtube" in link or "youtu.be" in link:
            await interaction.response.defer(thinking=True)
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
                await DB().add_to_queue([id, filename, interaction.user.id, "link"])
                logger.info(f"{id} not ready, added to queue.")
                await interaction.followup.send(
                    "It's not ready and there's no !stat for this."
                )
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
                dlchannel = await self.bot.fetch_channel(DL_CHANNEL)
                embed = download_ready(interaction.user, filename, link)
                logger.info(f"{id} ready.")
                await dlchannel.send(embed=embed)
        else:
            await interaction.response.send_message("Only supports youtube for now.")

    @app_commands.command(name="video")
    async def video(self, interaction: discord.Interaction, url: str):
        resolutions = [720, 480, 360, 240]
        # allowed = ["youtube", "youtu.be", "ok.ru", "vimeo", "dailymotion"]
        # if input in allowed:
        await interaction.response.defer(thinking=True)
        async with Conn() as resp:
            result = await resp.get_json(Urls.DEBRID_UNLOCK + url)
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
            await interaction.followup.send("No 1080p, 720p, 480p, 360p or 240p found.")
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
                await DB().add_to_queue([id, filename, interaction.user.id, "link"])
                logger.info(f"{id} not ready, added to queue.")
                # discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction
                await interaction.followup.send(
                    "It's not ready and there's no !stat for this."
                )
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
                dlchannel = await self.bot.fetch_channel(DL_CHANNEL)
                embed = download_ready(interaction.user, filename, link)
                logger.info(f"{id} ready.")
                await dlchannel.send(embed=embed)
        except KeyError:
            link = result["data"]["link"]

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

    @commands.command(name="tiktest")
    async def tiktest(self, ctx, url):
        link = await get_tiktok_link(url)
        tt_file = await download_tiktok_video(link)
        logger.info(f"tt_file: {tt_file}")
        if tt_file == "Downloaded":
            file = discord.File("tiktok.mp4", filename="tiktok.mp4")
            await ctx.reply(file=file, mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "tiktok.com" in message.content:
            link = await get_tiktok_link(message.content)
            if link == 0:
                await message.add_reaction("‼️")
            tt_file = await download_tiktok_video(link)
            logger.info(f"tt_file: {tt_file}")
            if tt_file["status"] == 1:
                file = discord.File(
                    f"tiktok/{tt_file['fn']}.mp4", filename=f"{tt_file['fn']}.mp4"
                )
                tt_message = tt_file["url"].split("/", "")[-1]
                tt_message = tt_message.replace(".480.mp4", "")
                await message.delete()
                await message.channel.send(
                    f"<@{message.author.id}>\n{tt_message}", file=file
                )

                delete = await delete_file(f"tiktok/{tt_file['fn']}.mp4")
                if delete:
                    logger.info(f"Deleted {tt_file['fn']}.mp4")
                else:
                    logger.error(f"Failed to delete {tt_file['fn']}.p4")


async def setup(bot):
    await bot.add_cog(DirectDLCog(bot))
