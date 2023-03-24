import os
import glob
from discord import File
from discord.ext import commands
from loguru import logger
from config import ADMIN_ROLE, GITHUB_TOKEN
from utils.helpers import get_folder_time
from github import Github


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
        log_file = await self.get_log()
        await ctx.reply(file=File(log_file), mention_author=False)

    async def get_log(self):
        logs_folder = "/mnt/thumb/waffle/logs"
        log_file = max(
            glob.glob(os.path.join(logs_folder, "*.log")), key=os.path.getctime
        )
        return log_file

    async def create_issue(self, title, body):
        g = Github(os.environ["GITHUB_TOKEN"])
        repo = g.get_repo("idiotdoomspiral/waffle")
        issue = repo.create_issue(title=title, body=body)
        return issue

    @commands.command(name="bug", description="Report a bug.", brief="Report a bug.")
    async def bug(self, ctx, *, bug: str):
        logger.info(f"{ctx.author.name} reported a bug: {bug}")
        messages = [message async for message in ctx.channel.history(limit=5)]
        messages.reverse()
        messages = "\n".join([f"{m.author.name}: {m.content}" for m in messages])
        # log_file = await self.get_log()
        # with open(log_file, "r") as f:
        #    log = f.read()
        issue = await self.create_issue(
            title=bug,
            body=f"Last 20 messages:\n\n{messages}",
        )
        admin = await self.bot.fetch_user(ADMIN_ROLE)
        await admin.send(f"New bug reported: {issue.title}\n{issue.html_url}")
        await ctx.reply(
            f"Thanks for reporting a bug! I'll look into it as soon as possible.",
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
        logger.info(f"Syncing {len(synced)} commands.")
        await ctx.reply(f"Synced {len(synced)} commands.", mention_author=False)


async def setup(bot):
    await bot.add_cog(SystemCog(bot))
