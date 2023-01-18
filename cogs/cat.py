from discord.ext import commands
from loguru import logger
import config
import requests
import json


class CatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cat", aliases=["catgif", "neb"])
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
        await ctx.send(json.loads(requests.get(cat_search).text)[0]["url"])

    @commands.command(name="dog")
    async def dog(self, ctx):
        logger.info("Dog requested.")
        dog_search = (
            f"https://api.thedogapi.com/v1/images/search?api_key={config.dog_auth}"
        )
        dog_pic = json.loads(requests.get(dog_search).text)[0]["url"]
        await ctx.send(dog_pic)


def setup(bot):
    bot.add_cog(CatCog(bot))
