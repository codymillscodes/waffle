import os
import glob
from discord import File
from discord.ext import commands
from loguru import logger


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Ping waffle.", brief="Ping waffle.")
    async def ping(self, ctx):
        await ctx.reply("fuck you", mention_author=False)

    @commands.command(
        name="log",
        description="Uploads the most recent logfile.",
        brief="Uploads the most recent logfile.",
    )
    async def log(self, ctx):
        logger.info(f"{ctx.author.name} called log command.")
        if ctx.author.guild_permissions.administrator:
            logs_folder = "/mnt/thumb/waffle/logs"
            log_file = max(
                glob.glob(os.path.join(logs_folder, "*.log")), key=os.path.getctime
            )
            await ctx.reply(file=File(log_file), mention_author=False)
        else:
            await ctx.reply("lol youre not allowed to do this", mention_author=False)


def setup(bot):
    bot.add_cog(SystemCog(bot))
