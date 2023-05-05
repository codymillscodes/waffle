from discord.ext import commands
from discord import app_commands
import discord
from loguru import logger
import wikipediaapi as wiki
from howlongtobeatpy import HowLongToBeat
from udpy import AsyncUrbanClient
import fortnite_api
from fortnite_api.enums import TimeWindow
from typing import Literal
import config
import utils.embed
from utils.urls import Urls
from utils.connection import Connection as Conn


class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urban = AsyncUrbanClient()
        self.fnapi = fortnite_api.FortniteAPI(api_key=config.FORTNITE_API_KEY)
        self.hltb = HowLongToBeat(0.3)

    @app_commands.command(name="rs", description="Get runescape stats")
    async def runescape(self, interaction: discord.Interaction, user: str):
        logger.info(f"{interaction.user} wants {user}'s runescape stats.")
        user = user.replace(" ", "+")
        char_stats = []
        async with Conn() as resp:
            rs = await resp.get_text(Urls.RUNESCAPE3_HISCORE + user)
        for line in rs.splitlines():
            char_stats.append(line.split(","))
        stats_embed = utils.embed.runescape(user, char_stats)
        await interaction.response.send_message(embed=stats_embed)

    @app_commands.command(
        name="wiki",
        description="Search wikipedia. Kinda iffy for some reason.",
    )
    async def wiki(self, interaction: discord.Interaction, query: str):
        logger.info(f"{interaction.user} wants {query} from wikipedia.")
        wiki_search = wiki.Wikipedia("en")
        page = wiki_search.page(query)

        if page.exists():
            embed = utils.embed.wikipedia(page)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Pretty sure you made that up.")

    @app_commands.command(
        name="define",
        description="Get a definition from Urban Dictionary",
    )
    async def define(self, interaction: discord.Interaction, phrase: str):
        logger.info(f"{interaction.user} wants {phrase} defined.")
        if phrase == "random":
            defs = await self.urban.get_random_definition()
        else:
            defs = await self.urban.get_definition(phrase)
        try:
            await interaction.response.send_message(
                f"""**{defs[0].word}**\n`{defs[0].definition.replace("[", "").replace("]", "")}`\nEx: *{defs[0].example.replace("[", "").replace("]", "")}*"""
            )
        except IndexError as ex:
            logger.exception(ex)
            await interaction.response.send_message(
                "It's not in the urban dictionary. Maybe you should add it.",
            )

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
