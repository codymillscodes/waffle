from discord.ext import commands
from loguru import logger

# from utils import DB, embed


class RecoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # self.db = DB()

    @commands.slash_command(name="reco", description="Get a recommendation")
    async def add_reco(self, interaction: commands.Interaction, one: str):
        await interaction.response.send_message("one is " + one)
