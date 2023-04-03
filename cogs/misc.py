from discord.ext import commands
from random import randint
from loguru import logger


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("roll", description="Roll a dice"):
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        logger.info(f'{ctx.author} rolled {dice}')
        min = 1
        if 'd' not in dice and dice.isdigit():
            max = int(dice)
        elif 'd' in dice:
            min = int(dice.split('d')[0])
            max = int(dice.split('d')[1])
        else:
            await ctx.send('Invalid input')
            return
        
        if min > max:
            await ctx.send('Invalid input')
            return
        
        await ctx.send(f'You rolled a {randint(min, max)}')

    def setup(bot):
        bot.add_cog(MiscCog(bot))