import discord
from discord.ext import commands
from loguru import logger
from bs4 import BeautifulSoup
from utils.urls import Urls
from utils.connection import Connection as Conn


class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="waffle",
        description="Receive a random image from a forgotten time, from a forgotten place.",
        brief="Random image.",
    )
    async def waffle(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        logger.info("Image requested: waffle")
        async with Conn() as resp:
            r = await resp.get_text(Urls.WAFFLE_URL)
        image = BeautifulSoup(r, "html.parser").find("img").attrs["src"]
        logger.info(image)
        await interaction.followup.send(Urls.WAFFLE_URL + image, mention_author=False)


async def setup(bot):
    await bot.add_cog(ImagesCog(bot))
