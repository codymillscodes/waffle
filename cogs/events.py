from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and after.channel:
            if (
                before.self_stream
                or before.self_video
                and not after.self_stream
                or after.self_video
            ):
                print("You stopped streaming.")


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
