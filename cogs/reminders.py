from discord import app_commands
import discord
from loguru import logger
import parsedatetime as pdt
from datetime import datetime
from pytz import timezone
from utils.db import DB


class Reminders(app_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

    @app_commands.command()
    async def remindme(self, interaction: discord.Interaction, time: str, message: str):
        cal = pdt.Calendar()
        r_time = cal.parse(time, datetime.now(timezone("UTC")))
        new_time = datetime(*r_time[0][:6], tzinfo=timezone("UTC"))
        logger.info(r_time)
        await self.db.add_reminder(interaction.user.id, new_time, message)
