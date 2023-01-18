import discord
from discord.ext import commands

class TemplateCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name='repeat', aliases=['copy', 'mimic'])
    # async def do_repeat(self, ctx, *, our_input: str):
    #    await ctx.send(our_input)

def setup(bot):
    bot.add_cog(TemplateCog(bot))
