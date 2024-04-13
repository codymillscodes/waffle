import discord
from discord.ext import commands
from cogwatch import watch
from loguru import logger

# MY_GUILD = discord.Object(id=1196061028706951279)


class Waffle(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", description="waffle", intents=discord.Intents.all()
        )
        # self.tree = discord.app_commands.CommandTree(self)
        logger.add("logs/waffle.log", rotation="7 MB", retention="10 days")
        logger.level("DEBUG")
        logger.info("Logging is set up!")

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
