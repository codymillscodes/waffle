import discord
from discord.ext import commands
from discord.ext import tasks
from cogwatch import watch
from config import (
    TWITCH_CHANNEL,
    TWITCH_NOTIFY_ROLE,
    TWITCH_CLIENT_ID,
    TWITCH_SECRET,
    DL_CHANNEL,
    DEBRID_WEBDAV,
)
from loguru import logger
from utils.connection import Connection as Conn
import urllib.parse
from utils.urls import Urls
from utils.random import get_link_msg
from utils.embed import download_ready


class Waffle(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", description="waffle", intents=discord.Intents.all()
        )

        logger.add(
            "logs/{time}_waffle.log",
            rotation="7 MB",
        )
        logger.level("DEBUG")
        logger.info("Logging is set up!")

        self.twitch_headers = ""
        self.twitchers = []
        self.online = []

        with open("twitchers.txt") as f:
            for line in f:
                self.twitchers.append(line.rstrip("\n"))

    async def setup_hook(self):
        self.debrid_check.start()
        self.twitch_check.start()
        logger.info("Background tasks started.")

    @watch(path="cogs", preload=True)
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="8=====D~~"))
        logger.info(
            f"\n\nLogged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n"
        )
        logger.info("Successfully logged in and booted...!")
        logger.info("Cogwatch is running!")

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)

    @tasks.loop(seconds=15)
    async def twitch_check(self):
        twitch_channel = await self.fetch_channel(TWITCH_CHANNEL)
        # logger.debug("Checking twitchers...")
        for t in self.twitchers:
            async with Conn() as resp:
                stream_data = await resp.get_json(
                    Urls.TWITCH_URL + t, headers=self.twitch_headers
                )
            if len(stream_data["data"]) == 1:
                if t not in self.online:
                    self.online.append(t)
                    em_twitch = discord.Embed(description=f"<@&{TWITCH_NOTIFY_ROLE}>")
                    em_twitch.add_field(
                        name=f"""{t} is live: {stream_data["data"][0]["title"]} playing {stream_data["data"][0]["game_name"]}""",
                        value=f"{Urls.TWITCH_CHANNEL}{t}",
                    )
                    logger.info(f"{self.online} is online.")
                    await twitch_channel.send(embed=em_twitch)
            else:
                if t in self.online:
                    self.online.remove(t)
                    logger.info(f"{t} is offline.")

    @twitch_check.before_loop
    async def before_twitch_check(self):
        body = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_SECRET,
            "grant_type": "client_credentials",
        }
        async with Conn() as resp:
            keys = await resp.get_json(Urls.TWITCH_TOKEN_REQUEST, data=body)
        logger.info("Twitch token refreshed")
        self.twitch_headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": "Bearer " + keys["access_token"],
        }

    @tasks.loop(seconds=20)
    async def debrid_check(self):
        debrid = []
        # await self.twitch_check()
        with open("debrid.txt") as f:
            for line in f:
                temp_line = line.rstrip("\n").split(",")
                # temp_line[0] = re.sub("\D", '', temp_line[0])
                # temp_line[1] = re.sub("\D", '', temp_line[1])
                debrid.append(temp_line)
            f.close()
        if len(debrid) > 0:
            logger.info(f"{debrid}")
        for id in debrid:
            if id[2] == "link":
                logger.info(f"Checking: {id[0]}")
                async with Conn() as resp:
                    r = await resp.get_json(Urls.DEBRID_DELAYED + id[0])
                if r["data"]["status"] == 2:
                    link = r["data"]["link"]
                    link_split = link.split("/")[-2:]
                    filename = urllib.parse.unquote(link_split[1])
                    debrid.remove(id)
                    logger.info(f"removing {id[0]}")
                    with open("debrid.txt", "w") as f:
                        for line in debrid:
                            if line != f"{id[0]},{id[1]},{id[2]}":
                                f.write(f"{id[0]},{id[1]},{id[2]}")

                    embed = download_ready(id[1], filename, link)
                    dl_channel = await self.fetch_channel(DL_CHANNEL)
                    await dl_channel.send(embed=embed)
            else:
                try:
                    async with Conn() as resp:
                        status_json = await resp.get_json(
                            Urls.DEBRID_STATUS_ONE + id[0]
                        )
                except:
                    pass
                logger.info(f"Checking: {id[0]}")
                try:
                    if (
                        status_json["status"] == "error"
                        or status_json["data"]["magnets"]["statusCode"] > 4
                    ):
                        debrid.remove(id)
                        logger.info(f"removing {id[0]}")

                    if "Ready" in status_json["data"]["magnets"]["status"]:
                        with open("debrid.txt", "w") as f:
                            for line in debrid:
                                if line != f"{id[0]},{id[1]},magnet":
                                    f.write(f"{id[0]},{id[1]},magnet")

                        filename = status_json["data"]["magnets"]["filename"]
                        embed = download_ready(id[1], filename)
                        debrid.remove(id)
                        logger.info(f"Removed: {id}")
                        dl_channel = await self.fetch_channel(DL_CHANNEL)
                        await dl_channel.send(embed=embed)
                except:
                    pass

        with open("debrid.txt", "w") as f:
            for id in debrid:
                f.write(f"{id[0]},{id[1]},{id[2]}\n")

    @debrid_check.before_loop
    async def before_task(self):
        await self.wait_until_ready()
