from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waffle")
    async def waffle(self, ctx):
        waffles = "https://randomwaffle.gbs.fm/"
        image = (
            BeautifulSoup(requests.get(waffles).content, "html.parser")
            .find("img")
            .attrs["src"]
        )
        await ctx.send(waffles + image)


def setup(bot):
    bot.add_cog(MemeCog(bot))
