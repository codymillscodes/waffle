from discord.ext import commands
from loguru import logger
from bs4 import BeautifulSoup
from utils.urls import Urls
from utils.connection import Connection as Conn


class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="waffle",
        description="Receive a random image from a forgotten time, from a forgotten place.",
        brief="Random image.",
    )
    async def waffle(self, ctx):
        logger.info("Image requested: waffle")
        async with Conn() as resp:
            r = await resp.get_text(Urls.WAFFLE_URL)
        image = BeautifulSoup(r, "html.parser").find("img").attrs["src"]
        logger.info(image)
        await ctx.reply(Urls.WAFFLE_URL + image, mention_author=False)

    @commands.command(
        name="cat",
        aliases=["catgif", "neb"],
        description="CAT PICTURE!",
        brief="CAT PICTURE!",
    )
    async def cat(self, ctx):
        cmd = str(ctx.command)
        logger.info(f"Image requested: {cmd}")
        cat_search = ""
        if cmd == "cat":
            cat_search = Urls.CAT_RANDOM
        elif cmd == "catgif":
            cat_search = Urls.CAT_GIF
        elif cmd == "neb":
            cat_search = Urls.CAT_NEB

        async with Conn() as resp:
            j = await resp.get_json(cat_search)
        image = j[0]["url"]
        await ctx.reply(image, mention_author=False)


def setup(bot):
    bot.add_cog(ImagesCog(bot))
