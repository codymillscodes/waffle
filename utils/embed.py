from discord import Embed
from loguru import logger


def runescape(name, char_stats):
    embed = Embed(name=f"{name}'s stats", color=0x00FF00)
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
    logger.info(f"Built embed for {stats.user.name}")
    return embed


def htlb():
    pass
