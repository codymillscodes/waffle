from discord import app_commands
from discord.ext import commands
from random import randint
from loguru import logger
import discord
from utils.db import DB
from utils.embed import twitcher_embed, juiceme
from typing import Literal


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="juiceme", description="get relevant community urls")
    async def juiceme(self, interaction: discord.Interaction):
        logger.info(f"{interaction.user} wants to juice")
        await interaction.response.send_message(embed=juiceme())

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

    @app_commands.command(name="twitchers", description="Get twitcher status")
    async def twitchers(
        self, interaction: discord.Interaction, option: Literal["all", "online"]
    ):
        logger.info(f"{interaction.user} wants twitcher status")
        if option == "all":
            embed = twitcher_embed(await DB().get_twitchers(), False)
        elif option == "online":
            embed = twitcher_embed(await DB().get_twitchers(), True)
        await interaction.response.send_message(embed=embed)

    @commands.command(name="test", description="Test command")
    async def test(self, ctx):
        embed = discord.Embed(title="Test", description="Test")
        file = discord.File("test.mp4", filename="test.mp4")
        await ctx.send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(MiscCog(bot))
