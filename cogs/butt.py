from discord.ext import commands
import random
import inflect
from loguru import logger
from lib.buttwords import filter

p = inflect.engine()

message_count = 0
pause_count = 0


class ButtCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chance = 5
        self.filter = filter
        self.pause_count = 0

    def buttify(self, message):
        words = message.split()
        logger.info(f"Buttifying {message}")
        butt_num = random.randint(1, len(words) - 1)
        while words[butt_num] in self.filter or words[butt_num].startswith(":"):
            butt_num = random.randint(1, len(words) - 1)
        mod_word = words[butt_num]
        if "-" in mod_word:
            parts = mod_word.split("-")
            if random.choice([True, False]):
                words[butt_num] = "butt-" + parts[1]
            else:
                words[butt_num] = parts[0] + "-butt"
        else:
            if p.plural(mod_word) == mod_word:
                words[butt_num] = "butts"
            else:
                words[butt_num] = "butt"
        words[butt_num] = mod_word.lower()
        return " ".join(words)

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
            if (
                not message.content.startswith("!")
                and not "https://" in message.content
            ):
                if (
                    random.randint(1, 100) <= self.chance
                    and self.pause_count == 0
                    and "butt" not in message.content.lower()
                    and len(message.content.split()) > 3
                ):
                    new_message = self.buttify(message.content)

                    if new_message != message.content:
                        self.pause_count = random.randint(5, 15)
                        await message.channel.send(new_message)
                else:
                    if self.pause_count > 0:
                        self.pause_count -= 1


async def setup(bot):
    await bot.add_cog(ButtCog(bot))
