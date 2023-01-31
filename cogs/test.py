from py1337x import py1337x

torrents = py1337x(proxy="1337x.to")
results = torrents.search("living 2022", sortBy="seeders", order="desc")

x = []
for torrent in results["items"]:
    print(torrent["name"])
    info = torrents.info(torrentId=torrent["torrentId"])
    print(info["category"])
    if "xxx".upper() not in info["category"]:
        x.append(torrent)
    if len(x) > 5:
        break
print(x)
