from discord.ext import commands
import random
import inflect
from loguru import logger

p = inflect.engine()

message_count = 0
pause_count = 0


class ButtCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global message_count, pause_count

        if message.author == self.bot.user:
            return

        if self.bot.user in message.mentions:
            return

        if pause_count > 0:
            pause_count -= 1
            return

        new_message = ""
        words = message.content.split()

        
        if random.randint(1, 1000) <= 200:  # randomly decide whether to add "butt" to end of message
            logger.info(f"Buttifying {message.content}")
            for word in words:
                if word.startswith(":"):  # check if word is an emoji
                    new_word = word
                elif "-" in word:  # check if word is hyphenated
                    parts = word.split("-")
                    if random.choice(
                        [True, False]
                    ) and random.randint(1, 1000) <= 50"  # randomly decide which side to replace
                        new_word = "butt-" + parts[1]
                    else:
                        new_word = parts[0] + "-butt"
                else:
                    if (
                        p.plural(word) == word and random.randint(1, 1000) <= 200
                    ):  # randomly decide whether to pluralize with "butts"
                        new_word = "butts"
                    elif (
                        random.randint(1, 1000) <= 100
                    ):  # randomly decide whether to replace word with "butt"
                        new_word = "butt"
                    else:
                        new_word = word

                new_message += new_word + " "

            if (new_message != message.content):  # only send new message if it's different from original and random chance
                await message.channel.send(new_message)
                message_count += 1
                if message_count >= 3:  # randomly pause after every 3 messages
                    pause_count = random.randint(1, 100)
                    message_count = 0


async def setup(bot):
    await bot.add_cog(ButtCog(bot))
