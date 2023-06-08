from discord import app_commands
from discord.ext import commands
from random import randint
from loguru import logger
import discord


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name="test", description="Test command")
    async def test(self, ctx):
        embed = discord.Embed(title="Test", description="Test")
        file = discord.File("test.mp4", filename="test.mp4")
        await ctx.send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(MiscCog(bot))
