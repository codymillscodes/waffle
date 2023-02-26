from discord import Embed


def runescape_embed(name, char_stats):
    embed = Embed(name=f"{name}'s stats", color=0x00FF00)
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
    stats = char_stats[0 : len(stat_names)]
    stats = {}
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
    return embed
