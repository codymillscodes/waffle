import urllib.parse

import discord
from discord.ext import commands
from loguru import logger
from helpers.debrid import get_tiktok_link, download_tiktok_video, delete_file


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
