from discord.ext import commands
from random import randint
from loguru import logger
import discord


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

    @commands.command(name="test", description="Test command")
    async def test(self, ctx):
        embed = discord.Embed(url="https://7aseln.debrid.it//dl//2q83blj2c48//Every%20day%20is%20a%20step%20closer%21%20Its%20so%20great%20to%20spend%20life%20in%20school%20then%20at%20work%21%20%23work%20%23relatable%20%23corporate%20%23millennial%20%23millennialsoftiktok%20%23corporatehumor%20%23corporatemillennial%20%23workjokes%20%23corporatejokes%20%23workhumor%20%23officehumor%20.144.mp4, "title="Test", description="Test")
        await ctx.send(embed=embed)

    @commands.command(name="test2", description="Test command")
    async def test2(self, ctx):
        file = discord.File("test.mp4", filename="test.mp4")
        await ctx.send(file=file)

async def setup(bot):
    await bot.add_cog(MiscCog(bot))
