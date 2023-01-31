import config
import requests
import urllib.parse
from alldebrid_api import debrid_url
from discord.ext import commands
import aiohttp
import discord


class DirectDLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = config.debrid_key
        self.api_host = config.debrid_host
        self.token = ""
        self.session = aiohttp.ClientSession()

    # @commands.command(name="bandcamp")
    # async def status(self, ctx, *, url: str):
    #    os.system(f"bandcamp-dl --base-dir=/mnt/ext/music {url}")
    #    await ctx.send("Done! [ftp link]")

    @commands.command(name="unlock")
    async def unlock(self, ctx, *, input: str):
        agent = self.api_host
        key = self.api_key
        link = input
        url = debrid_url.create(
            "unlock",
            link=link,
            agent=agent,
            api_key=key,
        )
        result = requests.get(url).json()
        id = result["data"]["id"]
        filename = result["data"]["filename"]
        stream = urllib.parse.quote(result["data"]["streams"][0]["id"])
        stream_url = debrid_url.create(
            "streaming", agent=agent, api_key=key, id=id, stream=stream, link=link
        )
        r = requests.get(stream_url).json()
        id = r["data"]["delayed"]
        delay_url = debrid_url.create(
            "delayed", agent=agent, api_key=key, id=id, link=link
        )
        re = requests.get(delay_url).json()
        if re["data"]["status"] != 2:
            with open("debrid.txt", "a") as f:
                f.write(f"{id},{ctx.author.id},link\n")
            await ctx.send("It's not ready and there's no !stat for this.")
        elif re["data"]["status"] == 2:
            link = re["data"]["link"]
            dl_channel = await self.bot.fetch_channel(config.dl_channel)
            em_links = discord.Embed(description=f"{ctx.author.mention}")
            em_links.add_field(
                name={filename},
                value=f"[Click this shit for files, i am very lazy.]({link})",
            )
            await dl_channel.send(embed=em_links)
