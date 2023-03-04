from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            # Member joined voice channel
            voice_client = await after.channel.connect()
            # see if there is a stream
            stream = voice_client.stream
        if stream is not None:
            print("There is a stream in voice channel {0.name}".format(after.channel))
        else:
            print("There is no stream in voice channel {0.name}".format(after.channel))
        await voice_client.disconnect()


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
