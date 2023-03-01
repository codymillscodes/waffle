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
        self.chance = 15
        self.butt_count = 3

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

        if "roll tide" in message.content.lower():
            logger.info(f"Roll tide detected in {message.content}")
            await message.channel.send("Roll tide!")
        else:
            if (
                not message.content.startswith("!")
                and not "https://" in message.content
            ):
                if random.randint(1, 100) <= 20:
                    butts = 0
                    logger.info(f"Buttifying {message.content}")
                    previous_word = ""
                    for word in words:
                        if 'butt' in previous_word.lower():
                            new_word = word
                            continue
                        elif word.startswith(":"):
                            new_word = word
                        elif "-" in word:
                            parts = word.split("-")
                            if (
                                random.choice([True, False])
                                and random.randint(1, 100) <= self.chance and butts < self.butt_count
                            ):
                                new_word = "butt-" + parts[1]
                                butts += 1
                            else:
                                new_word = parts[0] + "-butt"
                                butts += 1
                        else:
                            if (
                                p.plural(word) == word
                                and random.randint(1, 100) <= self.chance - 5 and butts < self.butt_count
                            ):
                                new_word = "butts"
                                butts += 1
                            elif random.randint(1, 100) <= self.chance - 5 and butts < self.butt_count:
                                new_word = "butt"
                                butts += 1
                            else:
                                new_word = word

                        previous_word = word

                        new_message += new_word + " "
                    new_message = new_message.rstrip()
                    if new_message != message.content:
                        logger.info(f"New message: {new_message}")
                        logger.info(f"Original message: {message.content}")
                        await message.channel.send(new_message)
                        message_count += 1
                        if message_count >= 3:  # randomly pause after every 3 messages
                            pause_count = random.randint(1, 20)
                            message_count = 0


async def setup(bot):
    await bot.add_cog(ButtCog(bot))
