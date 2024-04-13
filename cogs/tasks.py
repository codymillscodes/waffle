from discord.ext import tasks, commands
from loguru import logger
from strings.urls import Urls
import helpers.embed
import helpers.db
import config
import httpx


class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.twitch_online = False
        # self.tiktok_online = False
        self.twitch_headers = {}
        self.stream_channel = 1196601048291352576
        self.twitchers = {}
        with open("twitchers.txt", "r") as f:
            for line in f:
                line = line.strip()
                self.twitchers[line] = False
        self.stream_monitor.start()

    @tasks.loop(seconds=30)
    async def stream_monitor(self):
        logger.info("Checking twitch")
        await self.check_twitch_stream_status()
        logger.info("Checking debrid queue")
        await self.debrid_check()

    async def check_twitch_stream_status(self):
        twitch_channel = await self.bot.fetch_channel(self.stream_channel)
        # logger.debug("Checking twitchers...")
        # logger.debug(f"Checking {len(self.twitchers)} twitchers...")
        for user in self.twitchers.keys():
            async with httpx.AsyncClient() as resp:
                stream_data = await resp.get(
                    f"https://api.twitch.tv/helix/streams?user_login={user}",
                    headers=self.twitch_headers,
                )
            try:
                if stream_data:
                    if "data" in stream_data:
                        if stream_data["data"] != []:
                            # logger.info(stream_data)
                            if stream_data["data"][0]["type"] == "live":
                                # logger.info(self.twitchers[user])
                                if not self.twitchers[user]:
                                    embed = helpers.embed.stream_embed(
                                        user,
                                        stream_data["data"][0]["title"],
                                        stream_data["data"][0]["game_name"],
                                    )
                                    self.twitchers[user] = True
                                    logger.info(f"{user} is online.")
                                    # await self.update_stream_channel(True)
                                    await twitch_channel.send("@everyone")
                                    await twitch_channel.send(embed=embed)
                        else:
                            if self.twitchers[user]:
                                self.twitchers[user] = False
                                logger.info(f"{user} is offline.")
                                # await self.update_stream_channel(False)
                    else:
                        logger.info(stream_data)
            except (KeyError, IndexError, UnboundLocalError) as e:
                logger.exception(e)
            except TypeError as e:
                logger.info("Twitch API is down.")
                logger.exception(e)

    async def get_twitch_headers(self):
        try:
            body = {
                "client_id": config.TWITCH_CLIENT_ID,
                "client_secret": config.TWITCH_SECRET,
                "grant_type": "client_credentials",
            }
            async with httpx.AsyncClient() as resp:
                keys = await resp.post_json(
                    "https://id.twitch.tv/oauth2/token", data=body
                )
            self.twitch_headers = {
                "Client-ID": config.TWITCH_CLIENT_ID,
                "Authorization": "Bearer " + keys["access_token"],
            }
            logger.info("Got twitch headers.")
        except Exception as e:
            logger.exception(e)
            pass

    @stream_monitor.before_loop
    async def before_twitch_check(self):
        # await self.wait_until_ready()
        await self.get_twitch_headers()

    async def debrid_check(self):
        # await self.twitch_check()

        queue = await self.db.get_active_queue()
        queue = list(queue)
        if len(queue) > 0:
            # logger.info(f"{queue}")
            for dl_id in queue:
                if "active" in dl_id["status"]:
                    # logger.info(f"Checking: {dl_id['task_id']}")
                    if "link" in dl_id["type"]:
                        async with httpx.AsyncClient() as resp:
                            r = await resp.get_json(
                                Urls.DEBRID_DELAYED + str(dl_id["task_id"])
                            )
                            logger.info(Urls.DEBRID_DELAYED + str(dl_id["task_id"]))
                            logger.debug(r)

                        if r["data"]["status"] == 2:
                            link = r["data"]["link"]
                            link_split = link.split("/")[-2:]
                            filename = urllib.parse.unquote(link_split[1])
                            logger.info(f"removing {dl_id['task_id']}")
                            await self.db.set_status(dl_id["task_id"], "complete")
                            embed = download_ready(
                                int(dl_id["user_id"]), filename, link
                            )
                            dl_channel = await self.fetch_channel(config.DL_CHANNEL)
                            await dl_channel.send(embed=embed)
                    else:
                        try:
                            async with Conn() as resp:
                                status_json = await resp.get_json(
                                    Urls.DEBRID_STATUS_ONE + str(dl_id["task_id"])
                                )
                        except Exception as e:
                            logger.exception(e)
                            pass
                        try:
                            if (
                                status_json["status"] == "error"
                                or status_json["data"]["magnets"]["statusCode"] > 4
                            ):
                                await self.db.set_status(dl_id["task_id"], "failed")
                                logger.info(f"removing {dl_id['task_id']}")

                            elif "Ready" in status_json["data"]["magnets"]["status"]:
                                await self.db.set_status(
                                    task_id=dl_id["task_id"], status="complete"
                                )
                                filename = status_json["data"]["magnets"]["filename"]
                                embed = download_ready(dl_id["user_id"], filename)
                                logger.info(f"Removed: {dl_id['task_id']}")
                                dl_channel = await self.fetch_channel(config.DL_CHANNEL)
                                await dl_channel.send(embed=embed)
                        except Exception as e:
                            logger.exception(e)
                            pass

async def setup(bot):
    await bot.add_cog(TasksCog(bot))
