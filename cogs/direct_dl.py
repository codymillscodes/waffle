import os
import re
import urllib.parse
import requests
from discord.ext import commands
import discord
from bs4 import BeautifulSoup
from loguru import logger
from alldebrid_api import debrid_url
import config


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.debrid_key
        self.api_host = config.debrid_host

    @commands.command(name="bandcamp")
    async def status(self, ctx, *, url: str):
        title = get_title(url)
        for t in range(len(title)):
            title[t] = re.sub(r"[^\w\s]", "", title[t].lower())
            title[t] = re.sub(r"\s+", "-", title[t])
        os.system(
            f"sh /mnt/thumb/waffle/scripts/bandcamp.sh {url} {title[1]} {title[0]} &"
        )
        logger.info(f"Downloading {title[0]} by {title[1]}")
        await ctx.message.add_reaction(config.emoji)

    @commands.command(name="unlock")
    async def unlock(self, ctx, *, input: str):
        agent = self.api_host
        key = self.api_key
        if "youtube" in input:
            link = input
            url = debrid_url.create(
                "unlock",
                link=link,
                agent=agent,
                api_key=key,
            )
            result = requests.get(url, timeout=30).json()
            id = result["data"]["id"]
            filename = result["data"]["filename"]
            logger.info(f"Unlocking ({id}) : {filename}")
            stream = urllib.parse.quote(result["data"]["streams"][0]["id"])
            stream_url = debrid_url.create(
                "streaming", agent=agent, api_key=key, id=id, stream=stream, link=link
            )
            r = requests.get(stream_url, timeout=30).json()
            id = r["data"]["delayed"]
            logger.info(f"Got delayed ID: {id}")
            delay_url = debrid_url.create(
                "delayed", agent=agent, api_key=key, id=id, link=link
            )
            re = requests.get(delay_url, timeout=30).json()
            if re["data"]["status"] != 2:
                with open("debrid.txt", "a") as f:
                    f.write(f"{id},{ctx.author.id},link\n")
                logger.info(f"{id} not ready, added to queue.")
                await ctx.send("It's not ready and there's no !stat for this.")
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
                dl_channel = await self.bot.fetch_channel(config.dl_channel)
                em_links = discord.Embed(description=f"{ctx.author.mention}")
                em_links.add_field(
                    name={filename},
                    value=f"[Click this shit for files, i am very lazy.]({link})",
                )
                logger.info(f"{id} ready.")
                await dl_channel.send(embed=em_links)
        else:
            await ctx.reply("Only supports youtube for now.", mention_author=False)


def setup(bot):
    bot.add_cog(DirectDLCog(bot))


def get_title(url):
    r = requests.get(url, timeout=30).text
    soup = BeautifulSoup(r, "html.parser")
    s = soup.find("meta", property="og:title")
    title = s["content"].split(", by ")
    logger.info(f"Got title: {title}")
    return title
