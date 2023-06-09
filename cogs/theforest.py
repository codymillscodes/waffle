import discord
from discord import app_commands
from discord.ext import commands
from loguru import Logger


class ForestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forest_file = "foreststats.txt"
        self.forest_stats = {}

    async def write_forest_stats(self):
        with open(self.forest_file, "w") as f:
            for key, value in self.forest_stats.items():
                f.write(f"{key} - {value}\n")

    async def read_forest_stats(self):
        with open(self.forest_file, "r") as f:
            for line in f:
                line = line.split(" - ")
                self.forest_stats[line[0]] = line[1].strip("\n")

    async def check_forest_file(self):
        try:
            await self.read_forest_stats()
        except FileNotFoundError:
            await self.write_forest_stats()

    @app_commands.command(name="update_forest", description="Update forest stat")
    async def update_forest(
        self, interaction: discord.Interaction, stat: str, value: int
    ):
        await self.check_forest_file()
        if int > 1:
            self.forest_stats[stat] += value
        else:
            self.forest_stats[stat] += value
        await self.write_forest_stats()
        await interaction.response.send_message(f"Updated {stat} to {value}")

    @app_commands.command(name="foreststats", description="Get forest stats")
    async def foreststats(self, interaction: discord.Interaction):
        await self.read_forest_stats()
        embed = discord.Embed(title="Forest Stats")
        for key, value in self.forest_stats.items():
            embed.add_field(name=key, value=value)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ForestCog(bot))
