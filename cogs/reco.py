from discord.ext import commands
from discord import app_commands
from loguru import logger
from utils.db import DB
import discord

# from utils import DB, embed


class RecoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

    @app_commands.command(name="add_reco", description="Add a recommendation")
    async def add_reco(
        self,
        interaction: discord.Interaction,
        title: str,
        media_type: str,
        rating: int,
        receiver: discord.Member,
    ):
        await self.db.add_reco(
            [interaction.user.id, receiver.id, media_type, title, rating]
        )
        await interaction.response.send_message(
            f"Added {title} to {receiver}'s recommendations!"
        )

    @app_commands.command(name="get_reco", description="Get recommendations")
    async def get_reco(
        self, interaction: discord.Interaction, receiver: discord.Member
    ):
        reco_array = []
        reco = await self.db.get_reco(receiver.id)
        for r in reco:
            reco_array.append(f"{r['media title']}: {r['media type']} ({r['rating']})")
        if reco is None:
            await interaction.response.send_message("No recommendations found.")
        else:
            await interaction.response.send_message(
                f"{receiver}'s recommendations: {reco_array}"
            )


async def setup(bot):
    await bot.add_cog(RecoCog(bot))
