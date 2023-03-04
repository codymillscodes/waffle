from discord.ext import commands
from config import TWITCH_NOTIFY_ROLE, TWITCH_CHANNEL
from utils.embed import stream_embed
from loguru import logger


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and after.channel:
            twitch_channel = await self.bot.fetch_channel(TWITCH_CHANNEL)
            await twitch_channel.send(embed=stream_embed(member.name))
            if before.self_stream and not after.self_stream:
                logger.info(f"{member.name} stopped streaming")


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
