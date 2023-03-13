from discord import Embed
from loguru import logger
from hurry.filesize import size
from utils.helpers import percentage
from utils.random import get_link_msg
from config import DEBRID_WEBDAV, TWITCH_NOTIFY_ROLE
from urllib.parse import quote
from utils.urls import Urls


def runescape(name, char_stats):
    embed = Embed(title=f"{name}'s stats", color=0x00FF00)
    logger.info(f"Building embed for {name}")
    stat_names = [
        "Overall",
        "Attack",
        "Defence",
        "Strength",
        "Constitution",
        "Ranged",
        "Prayer",
        "Magic",
        "Cooking",
        "Woodcutting",
        "Fletching",
        "Fishing",
        "Firemaking",
        "Crafting",
        "Smithing",
        "Mining",
        "Herblore",
        "Agility",
        "Thieving",
        "Slayer",
        "Farming",
        "Runecrafting",
        "Hunter",
        "Construction",
        "Summoning",
        "Dungeoneering",
        "Divination",
        "Invention",
        "Archaeology",
    ]
    stats = {}
    char_stats = char_stats[0 : len(stat_names)]
    for i in range(len(char_stats)):
        stats[stat_names[i]] = char_stats[i][1]
        # combat level = ((max((str + atk), (mag * 2), (rng * 2)) * 1.3) + def + hp + (pray / 2) + (sum / 2)) / 4;
    combat_level = (
        (
            max(
                (int(stats["Strength"]) + int(stats["Attack"])),
                (int(stats["Magic"]) * 2),
                (int(stats["Ranged"]) * 2),
            )
            * 1.3
        )
        + int(stats["Defence"])
        + int(stats["Constitution"])
        + (int(stats["Prayer"]) / 2)
        + (int(stats["Summoning"]) / 2)
    ) / 4
    embed.add_field(name=f"__Overall__: {stats['Overall']}", value="", inline=False)
    embed.add_field(
        name="__Combat__",
        value=f"**Combat Level:** {int(combat_level)}\n**Attack**: {stats['Attack']}\n**Strength:** {stats['Strength']}\n**Defence:** {stats['Defence']}\n**Constitution:** {stats['Constitution']}\n**Ranged:** {stats['Ranged']}\n**Magic:** {stats['Magic']}\n**Prayer:** {stats['Prayer']}\n**Summoning:** {stats['Summoning']}",
        inline=True,
    )
    embed.add_field(
        name="__Gathering__",
        value=f"**Mining:** {stats['Mining']}\n**Woodcutting:** {stats['Woodcutting']}\n**Fishing:** {stats['Fishing']}\n**Farming:** {stats['Farming']}\n**Hunter:** {stats['Hunter']}\n**Divination:** {stats['Divination']}\n**Archaeology:** {stats['Archaeology']}",
        inline=True,
    )
    embed.add_field(
        name="__Crafting__",
        value=f"**Smithing:** {stats['Smithing']}\n**Crafting:** {stats['Crafting']}\n**Fletching:** {stats['Fletching']}\n**Runecrafting:** {stats['Runecrafting']}\n**Construction:** {stats['Construction']}\n**Herblore:** {stats['Herblore']}\n**Cooking:** {stats['Cooking']}\n**Firemaking:** {stats['Firemaking']}",
        inline=True,
    )
    embed.add_field(
        name="__Other__",
        value=f"**Slayer:** {stats['Slayer']} **Dungeoneering:** {stats['Dungeoneering']} **Agility:** {stats['Agility']}\n**Thieving:** {stats['Thieving']} **Invention:** {stats['Invention']}",
        inline=False,
    )
    logger.info(f"Built embed for {name}")
    return embed


def wikipedia(page):
    embed = Embed(title=page.title, url=page.fullurl, color=0x00FF00)
    embed.description = f"{page.summary[0:500]}..."
    logger.info(f"Built embed for {page.title}")
    return embed


def fortnite(stats):
    logger.info(f"Building embed for {stats.user.name}")
    embed = Embed(
        title=f"{stats.user.name}",
        description=f"**Battle Pass:** {stats.battle_pass.level}",
    )
    overall = stats.stats.all.overall
    solo = stats.stats.all.solo
    duo = stats.stats.all.duo
    squad = stats.stats.all.squad
    embed.add_field(
        name="__Overall__",
        value=f"**Matches(Win rate):** {overall.matches} (*{overall.win_rate}%*)\n**K/D(ratio):** {overall.kills}/{overall.deaths} (*{overall.kd}*)\n**Kills\\Match:** {overall.kills_per_match} | **Kills\\Min:** {overall.kills_per_min}\n**Minutes Played:** {overall.minutes_played} | **Players Outlived:** {overall.players_outlived}",
        inline=False,
    )
    embed.add_field(
        name="__Solo__",
        value=f"**Matches(Win rate):** {solo.matches} (*{solo.win_rate}%*)\n**K/D(ratio):** {solo.kills}/{solo.deaths} (*{solo.kd}*)\n**Kills\\Match:** {solo.kills_per_match} | **Kills\\Min:** {solo.kills_per_min}\n**Minutes Played:** {solo.minutes_played} | **Players Outlived:** {solo.players_outlived}",
        inline=False,
    )
    embed.add_field(
        name="__Duo__",
        value=f"**Matches(Win rate):** {duo.matches} (*{duo.win_rate}%*)\n**K/D(ratio):** {duo.kills}/{duo.deaths} (*{duo.kd}*)\n**Kills\\Match:** {duo.kills_per_match} | **Kills\\Min:** {duo.kills_per_min}\n**Minutes Played:** {duo.minutes_played} | **Players Outlived:** {duo.players_outlived}",
        inline=False,
    )
    embed.add_field(
        name="__Squad__",
        value=f"**Matches(Win rate):** {squad.matches} (*{squad.win_rate}%*)\n**K/D(ratio):** {squad.kills}/{squad.deaths} (*{squad.kd}*)\n**Kills\\Match:** {squad.kills_per_match} | **Kills\\Min:** {squad.kills_per_min}\n**Minutes Played:** {squad.minutes_played} | **Players Outlived:** {squad.players_outlived}",
        inline=False,
    )
    logger.info(f"Built embed for {stats.user.name}")
    return embed


def hltb(name, results):
    logger.info(f"Building embed for {results[0].game_name}")
    embed = Embed(
        title=f"HLTB Results for {name}",
        url="https://howlongtobeat.com?q=" + name.replace(" ", "+"),
    )
    embed.set_thumbnail(url=results[0].game_image_url)
    if len(results) < 5:
        for x in results:
            platforms = ""
            for p in x.profile_platforms:
                platforms += f"{p}, "
            embed.add_field(
                name=f"{x.game_name} ({x.release_world})",
                value=f"**Dev:** {x.profile_dev}\n**Platforms:** {platforms[:-2]}\n**Main Story:** {x.main_story}h | **Main + Extras:** {x.main_extra}h\n**Completionist:** {x.completionist}h | **All:** {x.all_styles}h\n{x.game_web_link}",
                inline=False,
            )
    else:
        for i in range(4):
            platforms = ""
            for p in results[i].profile_platforms:
                platforms += f"{p}, "
            embed.add_field(
                name=f"{results[i].game_name} ({results[i].release_world}))",
                value=f"**Dev:** {results[i].profile_dev}\n**Platforms:** {platforms[:-2]}\n**Main Story:** {results[i].main_story}h | **Main + Extras:** {results[i].main_extra}h\n**Completionist:** {results[i].completionist}h | **All:** {results[i].all_styles}h\n{results[i].game_web_link}",
                inline=False,
            )
    logger.info(f"Built embed for {results[0].game_name}")
    return embed


# debrid embeds
def debrid_status(all_status):
    embed = Embed(title="__Download Status__", color=0x00FF00)
    for m in all_status:
        try:
            name = all_status[m].get("filename", "")
            dlsize = float(all_status[m].get("size", 0))
            seeders = all_status[m].get("seeders", 0)
            speed = all_status[m].get("downloadSpeed", 0)
            complete = float(all_status[m].get("downloaded", 0))
        except TypeError:
            name = m.get("filename", "")
            dlsize = float(m.get("size", 0))
            seeders = m.get("seeders", 0)
            speed = m.get("downloadSpeed", 0)
            complete = float(m.get("downloaded", 0))

        sized_size = 0
        percentage_complete = "0%"
        if dlsize > 0:
            sized_size = size(int(dlsize))
        if speed > 0:
            speed = size(int(speed))
        if complete > 0:
            percentage_complete = percentage(complete, dlsize)
        embed.add_field(
            name=name,
            value=f"{percentage_complete} of {sized_size} | Seeders: {seeders} | Speed: {speed}",
            inline=False,
        )
    return embed


def download_ready(author, magnet, link=None):
    embed = Embed(description=f"<@{author}>")
    if link is None:
        link = f"{DEBRID_WEBDAV}magnets/{quote(magnet)}/"
    embed.add_field(
        name=f"{magnet}",
        value=f"[{get_link_msg()}]({link})",
    )
    return embed


def torrent_results(results, emergency: bool = False):
    if emergency:
        embed = Embed(
            description=":rotating_light::bangbang:__***YOU HAVE DECLARED A TORRENT EMERGENCY***__:bangbang::rotating_light:"
        )
        if len(results["torrent_results"]) > 10:
            results = results["torrent_results"][:10]
        else:
            results = results["torrent_results"]
        x = 0
        for m in results:
            x = x + 1
            result_value = f"Seeders: {m['seeders']} | Leechers: {m['leechers']} | Size: {size(int(m['size']))}"
            embed.add_field(name=f"{x}. {m['title']}", value=result_value, inline=False)

        embed.add_field(
            name="----------------",
            value=f"More results, longer timeout. Don't fuck it up cause it probably won't work twice in a row!\n*!pick 1-{len(results)}*",
            inline=False,
        )
        return embed
    else:
        embed = Embed()
        if len(results) > 5:
            results = results[:5]
        x = 0
        for torrent in results:
            result_value = f"Seeders: {torrent['seeders']} | Leechers: {torrent['leechers']} | Size: {torrent['size']}"
            embed.add_field(
                name=f"{x+1}. {torrent['name']}",
                value=result_value,
                inline=False,
            )
            x = x + 1
        embed.add_field(
            name="----------------",
            value="You should pick the one with the most seeders and a reasonable filesize. Pay attention to the quality. You dont want a cam or TS.\n*!pick 1-5*",
            inline=False,
        )
        return embed


def stream_embed(name, title=None, game=None):
    embed = Embed(description=f"<@&{TWITCH_NOTIFY_ROLE}>")
    if title is not None:
        embed.add_field(
            name=f"""{name} is live: {title} playing {game}""",
            value=f"{Urls.TWITCH_CHANNEL}{name}",
        )
    else:
        embed.add_field(
            name=f"----------------",
            value=f"<@{name}> is live in the voice channel!",
        )
    return embed
