from discord.ext import commands
from discord import app_commands
from loguru import logger
from utils.db import DB
from utils.embed import reco_embed
from random import randint
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
        receiver: discord.Member,
    ):
        await self.db.add_reco([interaction.user.id, receiver.id, media_type, title])
        await interaction.response.send_message(
            f"Added {title} to {receiver}'s recommendations!"
        )

    @app_commands.command(name="get_reco", description="Get recommendations")
    async def get_reco(
        self, interaction: discord.Interaction, receiver: discord.Member = None
    ):
        if receiver is None:
            receiver = interaction.user
        reco = await self.db.get_reco(receiver.id)
        if reco is None:
            await interaction.response.send_message("No recommendations found.")
        else:
            embed = reco_embed(receiver.name, reco)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="random_reco", description="Get random recommendations")
    async def random_reco(self, interaction: discord.Interaction, amount: int):
        amount = amount + 1
        reco = await self.db.get_reco(interaction.user.id)
        if reco is None:
            await interaction.response.send_message("No recommendations found.")
        elif len(reco) < amount:
            await interaction.response.send_message(
                f"You have {len(reco)} recommendations. Just use /get_reco."
            )
        else:
            embed = reco_embed(interaction.user.name, reco, random=True, amount=amount)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="consumed", description="Mark a recommendation as watched"
    )
    async def consumed(
        self, interaction: discord.Interaction, number: int, rating: int
    ):
        r = await self.db.set_reco_consumed(number, rating)
        if r > 0:
            await interaction.response.send_message("Marked as watched!")
        else:
            await interaction.response.send_message("Recommendation not found.")

    @app_commands.command(
        name="get_consumed", description="Get watched recommendations"
    )
    async def get_consumed(
        self, interaction: discord.Interaction, receiver: discord.Member
    ):
        reco = await self.db.get_consumed_reco(receiver.id)
        embed = reco_embed(receiver.name, reco, consumed=True)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(RecoCog(bot))
