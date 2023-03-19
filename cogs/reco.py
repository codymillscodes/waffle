from discord.ext import commands
from discord import app_commands
from loguru import logger
import discord

# from utils import DB, embed


class RecoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # self.db = DB()

    @app_commands.command(name="add_reco", description="Add a recommendation")
    async def add_reco(
        self,
        interaction: discord.Interaction,
        title: str,
        type: str,
        rating: int,
        receiver: discord.Member,
    ):
        self.db.add_reco([interaction.user.id, receiver.id, type, title, rating])
        await interaction.response.send_message(
            f"Added {title} to {receiver}'s recommendations!"
        )


async def setup(bot):
    await bot.add_cog(RecoCog(bot))
