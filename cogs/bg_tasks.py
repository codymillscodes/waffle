from discord.ext import tasks
from discord.ext import commands
import discord
import requests
import json
import config
import urllib.parse
import random
from loguru import logger


class BGTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_headers = ""
        self.twitchers = []
        self.online = []
        with open("twitchers.txt") as f:
            for line in f:
                self.twitchers.append(line.rstrip("\n"))

    async def twitch_check(self):
        twitch_channel = await self.bot.fetch_channel(config.twitch_channel)
        for t in self.twitchers:
            stream = requests.get(
                "https://api.twitch.tv/helix/streams?user_login=" + t,
                headers=self.twitch_headers,
                timeout=10,
            )
            stream_data = stream.json()
            if len(stream_data["data"]) == 1:
                if t not in self.online:
                    self.online.append(t)
                    em_twitch = discord.Embed(
                        description=f"<@&{config.twitch_notify_role}>"
                    )
                    em_twitch.add_field(
                        name=f"""{t} is live: {stream_data["data"][0]["title"]} playing {stream_data["data"][0]["game_name"]}""",
                        value=f"https://www.twitch.tv/{t}",
                    )
                    logger.info(f"{self.online} is online.")
                    await twitch_channel.send(embed=em_twitch)
            else:
                if t in self.online:
                    self.online.remove(t)
                    logger.info(f"{t} is offline.")

    @tasks.loop(minutes=1)
    async def debrid_check(self):
        debrid = []
        link_msg = [
            "Click this shit for files, i am very lazy.",
            "linky linky",
            "this is a link",
            "3=====D~~",
        ]
        await self.twitch_check()
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
            status_url = f"https://api.alldebrid.com/v4/magnet/status?agent={config.debrid_host}&apikey={config.debrid_key}&id="
            try:
                status_json = json.loads(requests.get(f"{status_url}{id[0]}").text)
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
                            if line != f"{id[0]},{id[1]}":
                                f.write(f"{id[0]},{id[1]}")
                    em_links = discord.Embed(description=f"<@{id[1]}>")
                    filename = status_json["data"]["magnets"]["filename"]
                    link = f"{config.http_url}magnets/{urllib.parse.quote(filename)}/"
                    em_links.add_field(
                        name=f"{filename}",
                        value=f"[{random.choice(link_msg)}]({link})",
                    )
                    debrid.remove(id)
                    logger.info(f"Removed: {id}")
                    dl_channel = await self.bot.fetch_channel(config.dl_channel)
                    await dl_channel.send(embed=em_links)

            except:
                pass

        with open("debrid.txt", "w") as f:
            for id in debrid:
                f.write(f"{id[0]},{id[1]}\n")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("debridbg() ready!")
        self.debrid_check.start()
        body = {
            "client_id": config.twitch_client_id,
            "client_secret": config.twitch_secret,
            "grant_type": "client_credentials",
        }
        r = requests.post("https://id.twitch.tv/oauth2/token", body)
        # data output
        keys = r.json()
        # logger.debug(keys)
        self.twitch_headers = {
            "Client-ID": config.twitch_client_id,
            "Authorization": "Bearer " + keys["access_token"],
        }
        # logger.debug(self.twitch_headers)


def setup(bot):
    bot.add_cog(BGTasks(bot))
