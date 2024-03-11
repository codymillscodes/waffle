import discord
from discord.ext import commands
from discord import app_commands
from loguru import logger
import utils.hd2


class HelldiversCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hd2events", description="Get active Helldivers events")
    async def hd2events(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        logger.info("hd2 events requested.")
        events = await utils.hd2.helldivers_events()
        for e in events:
            embed = discord.Embed(title=e["title"], description=e["message"])
            await interaction.followup.send(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(HelldiversCog(bot))
