from discord.ext import commands
from loguru import logger
import wikipediaapi as wiki
from howlongtobeatpy import HowLongToBeat
from udpy import AsyncUrbanClient
import fortnite_api
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

    @commands.command(
        name="rs", description="Get runescape stats", brief="Get rs stats"
    )
    async def runescape(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg}'s runescape stats.")
        arg = arg.replace(" ", "+")
        char_stats = []
        async with Conn() as resp:
            rs = await resp.get_text(Urls.RUNESCAPE3_HISCORE + arg)
        for line in rs.splitlines():
            char_stats.append(line.split(","))
        stats_embed = utils.embed.runescape(arg, char_stats)
        await ctx.reply(embed=stats_embed, mention_author=False)

    @commands.command(
        name="wiki",
        description="Search wikipedia. Kinda iffy for some reason.",
        brief="Search wikipedia. Kinda iffy.",
    )
    async def wiki(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg} from wikipedia.")
        wiki_search = wiki.Wikipedia("en")
        page = wiki_search.page(arg)

        if page.exists():
            embed = utils.embed.wikipedia(page)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("Pretty sure you made that up.", mention_author=False)

    @commands.command(
        name="define",
        description="Get a definition from Urban Dictionary",
        brief="Get a def from Urban Dictionary.",
    )
    async def define(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg} defined.")
        if arg == "random":
            defs = await self.urban.get_random_definition()
        else:
            defs = await self.urban.get_definition(arg)
        try:
            await ctx.reply(
                f"""**{defs[0].word}**\n`{defs[0].definition.replace("[", "").replace("]", "")}`\nEx: *{defs[0].example.replace("[", "").replace("]", "")}*""",
                mention_author=False,
            )
        except IndexError as ex:
            logger.exception(ex)
            await ctx.reply(
                "It's not in the urban dictionary. Maybe you should add it.",
                mention_author=False,
            )

    @commands.command(
        name="fn", description="Get fortnite stats", brief="Get fortnite stats."
    )
    async def fn(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg}'s fortnite stats.")
        try:
            stats = self.fnapi.stats.fetch_by_name(arg)
            embed = utils.embed.fortnite(stats)
            await ctx.reply(embed=embed, mention_author=False)
        except fortnite_api.errors.NotFound:
            await ctx.reply("That's not a real player.", mention_author=False)

    @commands.command(name="hltb", brief="Get how long to beat stats")
    async def howlong(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg}'s how long to beat stats.")
        try:
            results = await self.hltb.async_search(arg, similarity_case_sensitive=False)
            embed = utils.embed.hltb(arg, results)
            await ctx.reply(embed=embed, mention_author=False)
        except IndexError:
            await ctx.reply("That's not a real game.", mention_author=False)
        except Exception as ex:
            logger.exception(ex)


def setup(bot):
    bot.add_cog(SearchCog(bot))
