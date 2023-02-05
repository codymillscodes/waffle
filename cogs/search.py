import discord
from discord.ext import commands
import wikipediaapi as wiki
import datetime
from udpy import AsyncUrbanClient
import requests


class SearchCog(commands.Cog):
    # urban = AsyncUrbanClient()

    def __init__(self, bot):
        self.bot = bot
        self.urban = AsyncUrbanClient()

    @commands.command(name="hogwarts")
    async def hogwarts(self, ctx):
        r = requests.get(
            "https://api.xrel.to/v2/search/releases.json?q=hogwarts%20legacy&scene=true&p2p=true&limit=5"
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
            await ctx.send(embed=results_embed)

    @commands.command(name="wiki")
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
            await ctx.send(embed=wiki_embed)
        else:
            await ctx.send("Pretty sure you made that up.")

    @commands.command(name="define")
    async def define(self, ctx, *, arg):
        if "random" in arg:
            defs = await self.urban.get_random_definition()
        else:
            defs = await self.urban.get_definition(arg)
        try:
            await ctx.send(
                f"""**{defs[0].word}**\n`{defs[0].definition.replace("[", "").replace("]", "")}`\nEx: *{defs[0].example.replace("[", "").replace("]", "")}*"""
            )
        except IndexError:
            await ctx.send("It's not in the urban dictionary. Maybe you should add it.")


def setup(bot):
    bot.add_cog(SearchCog(bot))
