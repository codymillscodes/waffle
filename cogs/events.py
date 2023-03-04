from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and after.channel:
            if before.self_stream and not after.self_stream:
                await member.send("You stopped streaming.")


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
