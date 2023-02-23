import discord
from discord.ext import commands
from discord.ext import tasks
from cogwatch import Watcher
import config
from loguru import logger
import sys

coggers = [
    "cogs.misc",
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

# if __name__ == "__main__":
#    for cog in coggers:
#        bot.load_extension(cog)


@bot.event
async def on_ready():
    logger.info(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
    )
    await bot.change_presence(activity=discord.Game(name="8=====D~~"))
    logger.info("Successfully logged in and booted...!")
    watcher = Watcher(bot, path="cogs", preload=True)
    await watcher.start()
    logger.info("Cogwatch is running!")


bot.run(config.discord_bot_token, bot=True, reconnect=True)
