from discord.ext import commands
from loguru import logger
import discord

# from utils import DB, embed


class RecoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # self.db = DB()

    @commands.hybrid_command(name="reco")
    async def add_reco(self, interaction: discord.Interaction, one: str):
        await interaction.response.send_message("one is " + one)
