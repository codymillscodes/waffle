import datetime
import glob
import os
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from loguru import logger
import wikipediaapi as wiki
from udpy import AsyncUrbanClient
import config


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urban = AsyncUrbanClient()

    @commands.command(name="ping", description="Ping waffle.")
    async def ping(self, ctx):
        await ctx.reply("pong", mention_author=False)

    @commands.command(name="log", description="Uploads the most recent logfile.")
    async def log(self, ctx):
        logger.info(f"{ctx.author.name} called log command.")
        if ctx.author.guild_permissions.administrator:
            logs_folder = "/mnt/thumb/waffle/logs"
            log_file = max(
                glob.glob(os.path.join(logs_folder, "*.log")), key=os.path.getctime
            )
            await ctx.reply(file=discord.File(log_file), mention_author=False)
        else:

            await ctx.reply("lol youre not allowed to do this", mention_author=False)

    @commands.command(
        name="waffle",
        description="Receive a random from a forgotten time, from a forgotten place.",
    )
    async def waffle(self, ctx):
        waffles = "https://randomwaffle.gbs.fm/"
        image = (
            BeautifulSoup(requests.get(waffles, timeout=30).content, "html.parser")
            .find("img")
            .attrs["src"]
        )
        logger.info(image)
        await ctx.reply(waffles + image, mention_author=False)

    @commands.command(name="cat", aliases=["catgif", "neb"], description="CAT PICTURE!")
    async def cat(self, ctx):
        cmd = str(ctx.command)
        logger.info(f"Image requested: {cmd}")
        if cmd == "cat":
            cat_search = (
                f"https://api.thecatapi.com/v1/images/search?api_key={config.cat_auth}"
            )
        elif cmd == "catgif":
            cat_search = f"https://api.thecatapi.com/v1/images/search?mime_types=gif&api_key={config.cat_auth}"
        elif cmd == "neb":
            cat_search = f"https://api.thecatapi.com/v1/images/search?breed_ids=nebe&api_key={config.cat_auth}"
        await ctx.reply(
            (requests.get(cat_search, timeout=20).json())[0]["url"],
            mention_author=False,
        )

    @commands.command(name="hogwarts", description="Has Hogwarts Legacy been cracked?")
    async def hogwarts(self, ctx):
        r = requests.get(
            "https://api.xrel.to/v2/search/releases.json?q=hogwarts%20legacy&scene=true&p2p=true&limit=5",
            timeout=30,
        ).json()
        if r["total"] == 0:
            await ctx.send("No release yet.")
        else:
            results = r["p2p_results"]
            results_embed = discord.Embed()
            for x in results:
                results_embed.add_field(
                    name=f"{x['dirname']}", value=f"{x['link_href']},", inline=False
                )
            await ctx.reply(embed=results_embed, mention_author=False)

    @commands.command(
        name="wiki", description="Search wikipedia. Kinda iffy for some reason."
    )
    async def wiki(self, ctx, *, arg):
        wiki_search = wiki.Wikipedia("en")
        page = wiki_search.page(arg)

        if page.exists():
            wiki_embed = discord.Embed()
            wiki_embed.set_footer(
                text=f"{ctx.author} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            wiki_embed.description = (
                f"[**{page.title}**]({page.fullurl})\n{page.summary[0:500]}..."
            )
            await ctx.reply(embed=wiki_embed, mention_author=False)
        else:
            await ctx.reply("Pretty sure you made that up.", mention_author=False)

    @commands.command(
        name="define", description="Get a definition from Urban Dictionary"
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
        except IndexError as e:
            logger.exception(e)
            await ctx.reply(
                "It's not in the urban dictionary. Maybe you should add it.",
                mention_author=False,
            )


def setup(bot):
    bot.add_cog(MiscCog(bot))
