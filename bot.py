import discord
from discord.ext import commands
from discord.ext import tasks
import config
from loguru import logger
import sys

coggers = [
    "cogs.misc",
    "cogs.meme",
    "cogs.cat",
    "cogs.search",
    "cogs.chatbot",
    "cogs.debrid",
    "cogs.bg_tasks",
    "cogs.direct_dl",
]

bot = commands.Bot(command_prefix="!", description="waffle")

logger.add(
    "logs/{time}_waffle.log",
    rotation="7 MB",
)
logger.level("DEBUG")
logger.info("Logging is set up!")

if __name__ == "__main__":
    for cog in coggers:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    logger.info(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
    )
    await bot.change_presence(activity=discord.Game(name="8=====D~~"))
    logger.info(f"Successfully logged in and booted...!")


bot.run(config.discord_bot_token, bot=True, reconnect=True)
