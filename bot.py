import discord
from discord.ext import commands
from discord.ext import tasks
from cogwatch import watch
import config
from loguru import logger
import aiohttp


class Waffle(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", description="waffle")

        logger.add(
            "logs/{time}_waffle.log",
            rotation="7 MB",
        )
        logger.level("DEBUG")
        logger.info("Logging is set up!")
        self.session = aiohttp.ClientSession()

    @watch(path="cogs", preload=True)
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="8=====D~~"))
        logger.info(
            f"\n\nLogged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n"
        )
        logger.info("Successfully logged in and booted...!")
        logger.info("Cogwatch is running!")

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
