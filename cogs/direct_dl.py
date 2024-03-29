import os
import re
import urllib.parse

import discord
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands
from loguru import logger
from libgen_api import LibgenSearch

from config import DL_CHANNEL
from utils.connection import Connection as Conn
from utils.db import DB
from utils.debrid import get_tiktok_link, download_tiktok_video, delete_file
from utils.embed import download_ready
from utils.urls import Urls
from typing import Literal


async def get_title(url):
    async with Conn() as resp:
        r = await resp.get_text(url)
    soup = BeautifulSoup(r, "html.parser")
    s = soup.find("meta", property="og:title")
    title = s["content"].split(", by ")
    logger.info(f"Got title: {title}")
    return title


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.books = LibgenSearch()

    @app_commands.command(
        name="bandcamp",
        description="Download an album from Bandcamp. Gets uploaded to my server for downloading.",
    )
    async def bandcamp(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True)
        title = await get_title(url)
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
            yt_id = result["data"]["id"]
            filename = result["data"]["filename"]
            logger.info(f"Unlocking ({yt_id}) : {filename}")
            stream = urllib.parse.quote(result["data"]["streams"][0]["id"])
            async with Conn() as resp:
                result = await resp.get_json(
                    f"{Urls.DEBRID_STREAMING}{yt_id}&stream={stream}"
                )
            yt_id = result["data"]["delayed"]
            logger.info(f"Got delayed ID: {yt_id}")
            async with Conn() as resp:
                resp = await resp.get_json(Urls.DEBRID_DELAYED + str(yt_id))
            if resp["data"]["status"] != 2:
                await DB().add_to_queue([yt_id, filename, interaction.user.id, "link"])
                logger.info(f"{yt_id} not ready, added to queue.")
                await interaction.followup.send(
                    "It's not ready and there's no !stat for this."
                )
            elif resp["data"]["status"] == 2:
                link = resp["data"]["link"]
                dl_channel = await self.bot.fetch_channel(DL_CHANNEL)
                embed = download_ready(interaction.user, filename, link)
                logger.info(f"{yt_id} ready.")
                await dl_channel.send(embed=embed)
        else:
            await interaction.response.send_message("Only supports youtube for now.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "tiktok.com" in message.content:
            link = await get_tiktok_link(message.content)
            if link == 0:
                await message.add_reaction("‼️")
            else:
                tt_file = await download_tiktok_video(link)
                logger.info(f"tt_file: {tt_file}")
                if tt_file["status"] == 1:
                    file = discord.File(
                        f"tiktok/{tt_file['fn']}.mp4", filename=f"{tt_file['fn']}.mp4"
                    )
                    tt_message = tt_file["url"].split("/")
                    tt_message = urllib.parse.unquote(
                        tt_message[-1].replace(".480.mp4", "")
                    )
                    logger.info(f"tt_message: {tt_message}")

                    await message.delete()
                    await message.channel.send(
                        f"<@{message.author.id}>\n>>> {tt_message}", file=file
                    )

                    delete = await delete_file(f"tiktok/{tt_file['fn']}.mp4")
                    if delete:
                        logger.info(f"Deleted {tt_file['fn']}.mp4")
                    else:
                        logger.error(f"Failed to delete {tt_file['fn']}.mp4")


async def setup(bot):
    await bot.add_cog(DirectDLCog(bot))
