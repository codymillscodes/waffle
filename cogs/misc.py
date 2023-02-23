import datetime
import glob
import os
import random
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from loguru import logger
import wikipediaapi as wiki
from howlongtobeatpy import HowLongToBeat
from udpy import AsyncUrbanClient
import fortnite_api
import config

TROLL = [
    "I am a wizard, not a baboon brandishing a stick.",
    "Don’t put your wand there, boy! … Better wizards than you have lost buttocks, you know.",
    "Why are you worrying about YOU-KNOW-WHO, when you should be worrying about YOU-NO-POO? The constipation sensation that’s gripping the nation!",
    "Anyone can speak Troll. All you have to do is point and grunt.",
    "Alas! Ear wax!",
    "A troll in the dungeon is worth two in the Forbidden Forest.",
    "Trolls, theyre just misunderstood boulders with attitudes.",
    "Trolls and toilets, they both have problems with clogging.",
]


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urban = AsyncUrbanClient()
        self.fnapi = fortnite_api.FortniteAPI(api_key=config.fortnite_api)
        self.hltb = HowLongToBeat(0.7)

    @commands.command(name="ping", description="Ping waffle.", brief="Ping waffle.")
    async def ping(self, ctx):
        await ctx.reply("pong", mention_author=False)

    @commands.command(
        name="log",
        description="Uploads the most recent logfile.",
        brief="Uploads the most recent logfile.",
    )
    async def log(self, ctx):
        logger.info(f"{ctx.author.name} called log command.")
        if ctx.author.guild_permissions.administrator:
            logs_folder = "/mnt/thumb/waffle/logs"
            log_file = max(
                glob.glob(os.path.join(logs_folder, "*.log")), key=os.path.getctime
            )
            await ctx.reply(file=discord.File(log_file), mention_author=False)
        else:

            await ctx.reply("lol youre not allowed to do this", mention_author=False)

    @commands.command(
        name="waffle",
        description="Receive a random image from a forgotten time, from a forgotten place.",
        brief="Random image.",
    )
    async def waffle(self, ctx):
        waffles = "https://randomwaffle.gbs.fm/"
        image = (
            BeautifulSoup(requests.get(waffles, timeout=30).content, "html.parser")
            .find("img")
            .attrs["src"]
        )
        logger.info(image)
        await ctx.reply(waffles + image, mention_author=False)

    @commands.command(
        name="cat",
        aliases=["catgif", "neb"],
        description="CAT PICTURE!",
        brief="CAT PICTURE!",
    )
    async def cat(self, ctx):
        cmd = str(ctx.command)
        logger.info(f"Image requested: {cmd}")
        if cmd == "cat":
            cat_search = (
                f"https://api.thecatapi.com/v1/images/search?api_key={config.cat_auth}"
            )
        elif cmd == "catgif":
            cat_search = f"https://api.thecatapi.com/v1/images/search?mime_types=gif&api_key={config.cat_auth}"
        elif cmd == "neb":
            cat_search = f"https://api.thecatapi.com/v1/images/search?breed_ids=nebe&api_key={config.cat_auth}"
        await ctx.reply(
            (requests.get(cat_search, timeout=20).json())[0]["url"],
            mention_author=False,
        )

    @commands.command(
        name="hogwarts",
        description="Has Hogwarts Legacy been cracked?",
        brief="Has Hogwarts Legacy been cracked?",
    )
    async def hogwarts(self, ctx):
        try:
            r = requests.get(
                "https://api.xrel.to/v2/search/releases.json?q=hogwarts%20legacy&scene=true&p2p=true&limit=5",
                timeout=30,
            ).json()
            if r["total"] == 0:
                await ctx.send("No Hogwarts crack yet.")
            else:
                results = r["p2p_results"]
                results_embed = discord.Embed()
                for x in results:
                    results_embed.add_field(
                        name=f"{x['dirname']}", value=f"{x['link_href']},", inline=False
                    )
                await ctx.reply(embed=results_embed, mention_author=False)
        except requests.exceptions.JSONDecodeError:
            await ctx.reply(random.choice(TROLL), mention_author=False)

    @commands.command(
        name="wiki",
        description="Search wikipedia. Kinda iffy for some reason.",
        brief="Search wikipedia. Kinda iffy.",
    )
    async def wiki(self, ctx, *, arg):
        wiki_search = wiki.Wikipedia("en")
        page = wiki_search.page(arg)

        if page.exists():
            wiki_embed = discord.Embed()
            wiki_embed.set_footer(
                text=f"{ctx.author} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            wiki_embed.description = (
                f"[**{page.title}**]({page.fullurl})\n{page.summary[0:500]}..."
            )
            await ctx.reply(embed=wiki_embed, mention_author=False)
        else:
            await ctx.reply("Pretty sure you made that up.", mention_author=False)

    @commands.command(
        name="define",
        description="Get a definition from Urban Dictionary",
        brief="Get a def from Urban Dictionary.",
    )
    async def define(self, ctx, *, arg):
        logger.info(f"{ctx.author.name} wants {arg} defined.")
        if arg == "random":
            defs = await self.urban.get_random_definition()
        else:
            defs = await self.urban.get_definition(arg)
        try:
            await ctx.reply(
                f"""**{defs[0].word}**\n`{defs[0].definition.replace("[", "").replace("]", "")}`\nEx: *{defs[0].example.replace("[", "").replace("]", "")}*""",
                mention_author=False,
            )
        except IndexError as e:
            logger.exception(e)
            await ctx.reply(
                "It's not in the urban dictionary. Maybe you should add it.",
                mention_author=False,
            )

    @commands.command(
        name="fn", description="Get fortnite stats", brief="Get fortnite stats."
    )
    async def fn(self, ctx, *, arg):
        try:
            stats = self.fnapi.stats.fetch_by_name(arg)
            stats_embed = discord.Embed(
                title=f"{stats.user.name}",
                description=f"**Battle Pass:** {stats.battle_pass.level}",
            )
            overall = stats.stats.all.overall
            solo = stats.stats.all.solo
            duo = stats.stats.all.duo
            squad = stats.stats.all.squad
            stats_embed.add_field(
                name="__Overall__",
                value=f"**Matches(Win rate):** {overall.matches} (*{overall.win_rate}%*)\n**K/D(ratio):** {overall.kills}/{overall.deaths} (*{overall.kd}*)\n**Kills\\Match:** {overall.kills_per_match} | **Kills\\Min:** {overall.kills_per_min}\n**Minutes Played:** {overall.minutes_played} | **Players Outlived:** {overall.players_outlived}",
                inline=False,
            )
            stats_embed.add_field(
                name="__Solo__",
                value=f"**Matches(Win rate):** {solo.matches} (*{solo.win_rate}%*)\n**K/D(ratio):** {solo.kills}/{solo.deaths} (*{solo.kd}*)\n**Kills\\Match:** {solo.kills_per_match} | **Kills\\Min:** {solo.kills_per_min}\n**Minutes Played:** {solo.minutes_played} | **Players Outlived:** {solo.players_outlived}",
                inline=False,
            )
            stats_embed.add_field(
                name="__Duo__",
                value=f"**Matches(Win rate):** {duo.matches} (*{duo.win_rate}%*)\n**K/D(ratio):** {duo.kills}/{duo.deaths} (*{duo.kd}*)\n**Kills\\Match:** {duo.kills_per_match} | **Kills\\Min:** {duo.kills_per_min}\n**Minutes Played:** {duo.minutes_played} | **Players Outlived:** {duo.players_outlived}",
                inline=False,
            )
            stats_embed.add_field(
                name="__Squad__",
                value=f"**Matches(Win rate):** {squad.matches} (*{squad.win_rate}%*)\n**K/D(ratio):** {squad.kills}/{squad.deaths} (*{squad.kd}*)\n**Kills\\Match:** {squad.kills_per_match} | **Kills\\Min:** {squad.kills_per_min}\n**Minutes Played:** {squad.minutes_played} | **Players Outlived:** {squad.players_outlived}",
                inline=False,
            )
            await ctx.reply(embed=stats_embed, mention_author=False)
        except fortnite_api.errors.NotFound:
            await ctx.reply("That's not a real player.", mention_author=False)

    @commands.command(name="hltb", brief="Get how long to beat stats")
    async def howlong(self, ctx, *, arg):
        try:
            results = await self.hltb.async_search(arg, similarity_case_sensitive=False)
            game_embed = discord.Embed(
                title=f"HLTB Results for {arg}",
                url="https://howlongtobeat.com",
            )
            game_embed.set_image(url=results[0].game_image_url)
            if len(results) < 5:
                for x in results:
                    platforms = ""
                    for p in x.profile_platforms:
                        platforms += f"{p}, "
                    game_embed.add_field(
                        name=f"{x.game_name} ({x.release_world})",
                        value=f"**Dev:** {x.profile_dev}\n**Platforms:** {platforms}\n**Main Story:** {x.main_story}h | **Main + Extras:** {x.main_extra}h\n**Completionist:** {x.completionist}h | **All:** {x.all_styles}h\n{x.game_web_link}",
                        inline=False,
                    )
            else:
                for i in range(5):
                    for p in results[i].profile_platforms:
                        platforms += f"{p}, "
                    game_embed.add_field(
                        name=f"{results[i].game_name} ({results[i].release_world}))",
                        value=f"**Dev:** {results[i].profile_dev}\n**Platforms:** {platforms}\n**Main Story:** {results[i].main_story}h | **Main + Extras:** {results[i].main_extra}h\n**Completionist:** {results[i].completionist}h | **All:** {results[i].all_styles}h\n{results[i].game_web_link}",
                        inline=False,
                    )
            await ctx.reply(embed=game_embed, mention_author=False)
        except Exception as e:
            logger.exception(e)
            await ctx.reply("That's not a real game.", mention_author=False)


def setup(bot):
    bot.add_cog(MiscCog(bot))
