from discord.ext import commands
from discord import app_commands
import discord
from loguru import logger
from howlongtobeatpy import HowLongToBeat
import fortnite_api
from fortnite_api.enums import TimeWindow
from typing import Literal
import config
import helpers.embed


class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fnapi = fortnite_api.FortniteAPI(api_key=config.FORTNITE_API_KEY)
        self.hltb = HowLongToBeat(0.3)

    @app_commands.command(name="fn", description="Get fortnite stats")
    async def fn(
        self,
        interaction: discord.Interaction,
        time: Literal["all-time", "seasonal"],
        user: str,
    ):
        logger.info(f"{interaction.user} wants {user}'s fortnite stats.")
        try:
            if time == "seasonal":
                stats = self.fnapi.stats.fetch_by_name(
                    user, time_window=TimeWindow.SEASON
                )
                embed = utils.embed.fortnite(stats)
                await interaction.response.send_message(embed=embed)
            elif time == "all-time":
                stats = self.fnapi.stats.fetch_by_name(user)
                embed = utils.embed.fortnite(stats)
                await interaction.response.send_message(embed=embed)
        except fortnite_api.errors.NotFound:
            await interaction.response.send_message("That's not a real player.")

    @app_commands.command(name="hltb", description="Get how long to beat stats")
    async def howlong(self, interaction: discord.Interaction, game: str):
        logger.info(f"{interaction.user} wants {game}'s how long to beat stats.")
        try:
            results = await self.hltb.async_search(
                game, similarity_case_sensitive=False
            )
            embed = utils.embed.hltb(game, results)
            await interaction.response.send_message(embed=embed)
        except IndexError:
            await interaction.response.send_message("That's not a real game.")
        except Exception as ex:
            logger.exception(ex)


async def setup(bot):
    await bot.add_cog(SearchCog(bot))
