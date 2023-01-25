import discord
from discord.ext import commands
import subprocess
import config
from loguru import logger


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sys_role = config.restart_role

    @commands.command(name="restartbot")
    async def restartbot(self, ctx):
        valid_role = 0
        for role in ctx.author.roles:
            if role.id == self.sys_role:
                valid_role = 1
        if valid_role == 1:
            subprocess.run("/mnt/thumb/waffle/scripts/restart.sh", shell=True)
            logger.info(f"{ctx.author} is restarting the bot.")
            await ctx.send("Bot restarting!")
        else:
            await ctx.send("You're no bot boy!")

    @commands.command(name="gitupdate")
    async def gitupdate(self, ctx):
        valid_role = 0
        for role in ctx.author.roles:
            if role.id == self.sys_role:
                valid_role = 1
        if valid_role == 1:
            subprocess.run("/waffle/scripts/update.sh", shell=True)
            logger.info(f"{ctx.author} is updating the bot.")
            await ctx.send("Bot updating!")
        else:
            await ctx.send("You're no bot boy!")


def setup(bot):
    bot.add_cog(SystemCog(bot))
