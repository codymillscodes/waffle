import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks
from cogwatch import watch
import config
from loguru import logger
import sys


class Waffle(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    @watch(path="cogs", preload=True, debug=False)
    async def on_ready(self):
        logger.add(
            "logs/{time}_waffle.log",
            rotation="7 MB",
        )
        logger.level("DEBUG")
        logger.info("Logging is set up!")
        logger.info(
            f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
        )
        await bot.change_presence(activity=discord.Game(name="8=====D~~"))
        logger.info("Successfully logged in and booted...!")

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)


async def main():
    client = Waffle()
    await client.start(config.discord_bot_token)
