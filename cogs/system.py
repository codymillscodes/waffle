import os
import glob
from discord import File
from discord.ext import commands
from loguru import logger


async def get_log():
    logs_folder = "/root/waffle/logs"
    log_file = max(glob.glob(os.path.join(logs_folder, "*.log")), key=os.path.getctime)
    return log_file


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @app_commands.command(name="leave", description="leave a guild by name")
    # async def leaveg(self, interaction: discord.Interaction, guild_name: str):
    #     guild = discord.utils.get(
    #         self.bot.guilds, name=guild_name
    #     )  # Get the guild by name
    #     if guild is None:
    #         print("No guild with that name found.")  # No guild found
    #         return
    #     await guild.leave()  # Guild found
    #     await interaction.response.send_message(f"I left: {guild.name}!")

    @commands.command(
        name="log",
        description="Uploads the most recent logfile.",
        brief="Uploads the most recent logfile.",
    )
    async def log(self, ctx):
        logger.info(f"{ctx.author.name} called log command.")
        log_file = await get_log()
        await ctx.reply(file=File(log_file), mention_author=False)

    @commands.command(name="sync")
    async def sync(self, ctx):
        guild = ctx.guild
        ctx.bot.tree.copy_global_to(guild=guild)
        synced = await ctx.bot.tree.sync()
        logger.info(f"Syncing {len(synced)} commands.")
        await ctx.reply(f"Synced {len(synced)} commands.", mention_author=False)


async def setup(bot):
    await bot.add_cog(SystemCog(bot))
