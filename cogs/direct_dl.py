import os
import re
import urllib.parse
from discord.ext import commands
import discord
from bs4 import BeautifulSoup
from loguru import logger
from alldebrid_api import debrid_url
from config import debrid_host, debrid_key, emoji, dl_channel


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = debrid_key
        self.api_host = debrid_host

    @commands.command(
        name="bandcamp",
        description="Download an album from Bandcamp. Gets uploaded to my server for downloading.",
        brief="Download ANY album from bandcamp.",
    )
    async def bandcamp(self, ctx, *, url: str):
        title = self.get_title(url)
        for t in range(len(title)):
            title[t] = re.sub(r"[^\w\s]", "", title[t].lower())
            title[t] = re.sub(r"\s+", "-", title[t])
        os.system(
            f"sh /mnt/thumb/waffle/scripts/bandcamp.sh {url} {title[1]} {title[0]} &"
        )
        logger.info(f"Downloading {title[0]} by {title[1]}")
        await ctx.message.add_reaction(emoji)

    @commands.command(
        name="unlock",
        description="At the moment, it only returns the mp3 of a youtube video.",
        brief="Get mp3 of YT video.",
    )
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
            async with self.bot.session.get(url) as resp:
                result = await resp.json()
            id = result["data"]["id"]
            filename = result["data"]["filename"]
            logger.info(f"Unlocking ({id}) : {filename}")
            stream = urllib.parse.quote(result["data"]["streams"][0]["id"])
            stream_url = debrid_url.create(
                "streaming", agent=agent, api_key=key, id=id, stream=stream, link=link
            )
            async with self.bot.session.get(stream_url) as resp:
                result = await resp.json()
            id = r["data"]["delayed"]
            logger.info(f"Got delayed ID: {id}")
            delay_url = debrid_url.create(
                "delayed", agent=agent, api_key=key, id=id, link=link
            )
            async with self.bot.session.get(delay_url) as resp:
                re = await resp.json()
            if re["data"]["status"] != 2:
                with open("debrid.txt", "a") as f:
                    f.write(f"{id},{ctx.author.id},link\n")
                logger.info(f"{id} not ready, added to queue.")
                await ctx.send("It's not ready and there's no !stat for this.")
            elif re["data"]["status"] == 2:
                link = re["data"]["link"]
                dlchannel = await self.bot.fetch_channel(dl_channel)
                em_links = discord.Embed(description=f"{ctx.author.mention}")
                em_links.add_field(
                    name={filename},
                    value=f"[Click this shit for files, i am very lazy.]({link})",
                )
                logger.info(f"{id} ready.")
                await dlchannel.send(embed=em_links)
        else:
            await ctx.reply("Only supports youtube for now.", mention_author=False)

    async def get_title(self, url):
        async with self.bot.session.get(url) as resp:
            r = await resp.text()
        soup = BeautifulSoup(r, "html.parser")
        s = soup.find("meta", property="og:title")
        title = s["content"].split(", by ")
        logger.info(f"Got title: {title}")
        return title

def setup(bot):
    bot.add_cog(DirectDLCog(bot))
