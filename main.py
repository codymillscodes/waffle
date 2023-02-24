from bot import Waffle
from config import discord_bot_token

bot = Waffle()

if __name__ == "__main__":
    bot.run(discord_bot_token)
