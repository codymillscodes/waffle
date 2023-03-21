import os
import glob
from discord import File
from discord.ext import commands
from loguru import logger
from utils.helpers import get_folder_time


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

    @commands.command(name="bug", description="Report a bug.", brief="Report a bug.")
    async def bug(self, ctx, *, bug: str):
        logger.info(f"{ctx.author.name} reported a bug: {bug}")
        bug_folder = "/mnt/thumb/waffle/bugs"
        messages = [
            message
            async for message in ctx.channel.history(limit=10, oldest_first=True)
        ]
        with open(
            f"{bug_folder}/{get_folder_time()} - {ctx.author.name}.txt", "wx"
        ) as f:
            for message in messages:
                f.write(f"{message.author.name}: {message.content}\n")
        await ctx.reply(
            "Thanks for reporting a bug! I'll look into it as soon as possible.",
            mention_author=False,
        )

    # @commands.command(name="clear")
    # async def clear(self, ctx):
    #     guild = ctx.guild
    #     synced = await ctx.bot.tree.sync(guild=guild)
    #     c = await ctx.bot.tree.fetch_commands(guild=guild)
    #     for i in c:
    #         ctx.bot.tree.remove_command(i.name, guild=guild)
    #     logger.info(f"Clearing {len(c)} commands.")
    #     synced = await ctx.bot.tree.sync(guild=guild)
    #     await ctx.reply(f"Synced {len(synced)} commands.", mention_author=False)

    @commands.command(name="sync")
    async def sync(self, ctx):
        guild = ctx.guild
        ctx.bot.tree.copy_global_to(guild=guild)
        synced = await ctx.bot.tree.sync()
        await ctx.reply(f"Synced {len(synced)} commands.", mention_author=False)


async def setup(bot):
    await bot.add_cog(SystemCog(bot))
