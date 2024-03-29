from random import randint
from discord.ext import commands
from loguru import logger
from lib.dracula import dracula

message_count = 0
pause_count = 0


class ButtCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chance = 2
        self.pause_count = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user in message.mentions:
            return

        if "roll tide" in message.content.lower():
            logger.info(f"Roll tide detected in {message.content}")
            await message.channel.send("Roll tide!")
        else:
            if not (message.content.startswith("!") or "https://" in message.content):
                if randint(1, 100) <= self.chance and self.pause_count == 0:
                    new_message = dracula[randint(0, len(dracula))]

                    if new_message != message.content:
                        self.pause_count = randint(15, 50)
                        await message.channel.send(new_message)
                else:
                    if self.pause_count > 0:
                        self.pause_count -= 1


async def setup(bot):
    await bot.add_cog(ButtCog(bot))
