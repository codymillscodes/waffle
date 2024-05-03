from discord.ext import tasks, commands
from loguru import logger
import httpx
from strings.urls import Urls
import helpers.embed
import helpers.db
import config
from twitchAPI.twitch import Twitch


class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.twitch_online = False
        # self.tiktok_online = False
        self.stream_channel = 1196601048291352576
        self.twitchers = {}
        self.db = helpers.db.DB()
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
        auth = await Twitch(config.TWITCH_CLIENT_ID, config.TWITCH_SECRET)
        print(self.twitchers)
        try:
            users = list(self.twitchers.keys())
            async for s in Twitch.get_streams(auth, user_login=users):
                if s.user_login in users:
                    logger.info(s.user_login + " online.")

                    if not self.twitchers[s.user_login]:
                        embed = helpers.embed.stream_embed(
                            s.user_login,
                            s.title,
                            s.game_name,
                        )
                        self.twitchers[s.user_login] = True
                        logger.info(f"{s.user_login} is online.")
                        # await self.update_stream_channel(True)
                        await twitch_channel.send("<@&1196954735647920230>")
                        await twitch_channel.send(embed=embed)
                    else:
                        if self.twitchers[s.user_login]:
                            self.twitchers[s.user_login] = False
                            logger.info(f"{s.user_login} is offline.")
                            # await self.update_stream_channel(False)
                        # else:
                        #     logger.info(stream_data)
        except (KeyError, IndexError, UnboundLocalError) as e:
            logger.exception(e)
        except TypeError as e:
            logger.info("Twitch API is down.")
            logger.exception(e)

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
                            r = await resp.get(
                                Urls.DEBRID_DELAYED + str(dl_id["task_id"])
                            )
                        r = r.json()
                        logger.info(Urls.DEBRID_DELAYED + str(dl_id["task_id"]))
                        logger.debug(r)

                        if r["data"]["status"] == 2:
                            link = r["data"]["link"]
                            link_split = link.split("/")[-2:]
                            filename = urllib.parse.unquote(link_split[1])
                            logger.info(f"removing {dl_id['task_id']}")
                            await self.db.set_status(dl_id["task_id"], "complete")
                            embed = helpers.embed.download_ready(
                                int(dl_id["user_id"]), filename, link
                            )
                            dl_channel = await self.fetch_channel(config.DL_CHANNEL)
                            await dl_channel.send(embed=embed)
                    else:
                        try:
                            async with httpx.AsyncClient() as resp:
                                status_json = await resp.get(
                                    Urls.DEBRID_STATUS_ONE + str(dl_id["task_id"])
                                )
                            status_json = status_json.json()
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
                                embed = helpers.embed.download_ready(dl_id["user_id"], filename)
                                logger.info(f"Removed: {dl_id['task_id']}")
                                dl_channel = await self.fetch_channel(config.DL_CHANNEL)
                                await dl_channel.send(embed=embed)
                        except Exception as e:
                            logger.exception(e)
                            pass

async def setup(bot):
    await bot.add_cog(TasksCog(bot))
