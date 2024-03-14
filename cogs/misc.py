from discord import app_commands
from discord.ext import commands
from random import randint
from loguru import logger
import discord
from utils.urls import Urls
from bs4 import BeautifulSoup
import httpx


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="waffle",
        description="Receive a random image from a forgotten time, from a forgotten place.",
    )
    async def waffle(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        logger.info("Image requested: waffle")
        async with httpx.AsyncClient() as resp:
            r = await resp.get(Urls.WAFFLE_URL).text
        image = BeautifulSoup(r, "html.parser").find("img").attrs["src"]
        logger.info(image)
        await interaction.followup.send(Urls.WAFFLE_URL + image, mention_author=False)

    @app_commands.command(name="roll", description="Roll a dice")
    async def roll(self, interaction: discord.Interaction, num: int, faces: int):
        """Rolls a die in NdN format."""
        logger.info(f"{interaction.user} rolled {num}d{faces}")
        rolls = []
        for i in range(num):
            rolls.append(randint(1, faces))
        if len(rolls) == 1:
            await interaction.response.send_message(f"You rolled a {rolls[0]}")
        elif len(rolls) > 1:
            await interaction.response.send_message(
                f"You rolled {rolls} = {sum(rolls)}"
            )
        else:
            await interaction.response.send_message("Invalid input")


async def setup(bot):
    await bot.add_cog(MiscCog(bot))
