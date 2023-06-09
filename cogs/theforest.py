import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger
from datetime import datetime


class ForestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forest_file = "foreststats.txt"
        self.forest_logfile = "forestlog.txt"
        self.forest_stats = {}
        self.forest_log = ""

    async def write_forest_stats(self):
        logger.info("Writing forest stats")
        with open(self.forest_file, "w") as f:
            for key, value in self.forest_stats.items():
                f.write(f"{key} - {value}\n")
        logger.info("Wrote forest stats")

    async def write_forest_log(self, user, action):
        logger.info("Writing forest log")
        with open(self.forest_logfile, "a") as f:
            f.write(f"{user} - {action}\n")
        logger.info("Wrote forest log")

    async def read_forest_log(self):
        logger.info("Reading forest log")
        with open(self.forest_logfile, "r") as f:
            for line in f:
                line = line.split(" - ")
                self.forest_log += f"{line[0]} - {line[1]}"
        logger.info("Read forest log")

    async def check_forest_log(self):
        logger.info("Checking forest log")
        try:
            await self.read_forest_log()
        except FileNotFoundError:
            logger.info("Forest log not found, creating.")
            await self.write_forest_log("user", "action")
        logger.info("Checked forest log")

    async def read_forest_stats(self):
        logger.info("Reading forest stats")
        with open(self.forest_file, "r") as f:
            for line in f:
                line = line.split(" - ")
                self.forest_stats[line[0]] = line[1].strip("\n")
        logger.info("Read forest stats")

    async def check_forest_file(self):
        logger.info("Checking forest file")
        try:
            await self.read_forest_stats()
        except FileNotFoundError:
            logger.info("Forest file not found, creating.")
            await self.write_forest_stats()
        logger.info("Checked forest file")

    @app_commands.command(name="forestlog", description="Get forest log")
    async def forestlog(self, interaction: discord.Interaction):
        logger.info(f"{interaction.user} wants the forest log.")
        await self.check_forest_log()
        await interaction.response.send_message(file=discord.File(self.forest_logfile))

    @app_commands.command(
        name="increment_forest_stat", description="Update forest stat"
    )
    async def increment_forest_stat(
        self, interaction: discord.Interaction, stat: str, value: int
    ):
        logger.info(f"{interaction.user} wants to increment {stat} by {value}.")
        await self.check_forest_file()
        if self.forest_stats.get(stat) is None:
            self.forest_stats[stat] = 0
        if value > 1:
            self.forest_stats[stat] += value
        else:
            self.forest_stats[stat] += value
        await self.write_forest_stats()
        await self.write_forest_log(
            interaction.user, f"{datetime.now}| {stat} + {value}"
        )
        logger.info(f"Updated {stat} to {self.forest_stats[stat]}")
        await interaction.response.send_message(f"Updated {stat} to {value}")

    @app_commands.command(name="set_forest_stat", description="Update forest stat")
    async def set_forest_stat(
        self, interaction: discord.Interaction, stat: str, value: int
    ):
        logger.info(f"{interaction.user} wants to set {stat} to {value}.")
        await self.check_forest_file()
        if self.forest_stats.get(stat) is None:
            self.forest_stats[stat] = 0
        self.forest_stats[stat] = value
        await self.write_forest_stats()
        await self.write_forest_log(
            interaction.user, f"{datetime.now}| {stat} = {value}"
        )
        logger.info(f"Updated {stat} to {self.forest_stats[stat]}")
        await interaction.response.send_message(f"Updated {stat} to {value}")

    @app_commands.command(name="foreststats", description="Get forest stats")
    async def foreststats(self, interaction: discord.Interaction):
        logger.info(f"{interaction.user} wants the forest stats.")
        await self.read_forest_stats()
        embed = discord.Embed(title="Forest Stats")
        for key, value in self.forest_stats.items():
            embed.add_field(name=key, value=value, inline=False)
        logger.info(f"Sent forest stats.")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ForestCog(bot))
