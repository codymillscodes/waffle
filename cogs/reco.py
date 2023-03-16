from discord.ext import commands
from loguru import logger
import discord
import discord.app_commands

# from utils import DB, embed


class RecoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # self.db = DB()

    @discord.app_commands.command(name="add_reco", description="Add a recommendation")
    async def add_reco(self, interaction: discord.Interaction, one: str):
        await interaction.response.send_message("one is " + one)


async def setup(bot):
    await bot.add_cog(RecoCog(bot))
