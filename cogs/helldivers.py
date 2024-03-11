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
        # await interaction.response.defer(thinking=True)
        logger.info("hd2 events requested.")
        events = await utils.hd2.helldivers_events()
        embeds = []
        for e in events:
            embeds.append(discord.Embed(title=e["title"], description=e["message"]))

        await interaction.response.send_message(embeds=embeds)


async def setup(bot):
    await bot.add_cog(HelldiversCog(bot))
