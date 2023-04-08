from discord.ext import commands
from random import randint
from loguru import logger


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", description="Roll a dice")
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        logger.info(f"{ctx.author} rolled {dice}")
        min = 1
        if "d" not in dice and dice.isdigit():
            await ctx.send(f"You rolled a {randint(min, int(dice))}")
        elif "d" in dice:
            rolls = []
            num_to_roll = int(dice.split("d")[0])
            for i in range(num_to_roll):
                rolls.append(randint(1, int(dice.split("d")[1])))
            if len(rolls) == 1:
                await ctx.send(f"You rolled a {rolls[0]}")
            # send rolls '1 + 1 + 1 = 3' instead of [1, 1, 1], send the rseult of each roll and the total
            elif len(rolls) > 1:
                await ctx.send(f"You rolled {rolls} = {sum(rolls)}")
        else:
            await ctx.send("Invalid input")
            return


async def setup(bot):
    await bot.add_cog(MiscCog(bot))
