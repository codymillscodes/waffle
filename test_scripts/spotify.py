import json
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth as SPOauth
import pymongo

client = pymongo.MongoClient(
    f"mongodb+srv://waffle:5oaw7kQStm7pcd0P@waffle.i2tnxdm.mongodb.net/?retryWrites=true&w=majority"
)
db = client["waffle"]
plc = db["playlist"]
SPOTIPY_CLIENT_ID = "a8561f34dd374fff92d3931f88e72678"
SPOTIPY_CLIENT_SECRET = "3e0c8dd3b32d475ca29e8d9e8baaa7dd"
SPOTIPY_REDIRECT_URI = "http://localhost"

PLAYLIST_ID = (
    "https://open.spotify.com/playlist/6xHdV7jlRcuon1AaUDVvNb?si=89838e46b5484065"
)
# PLAYLIST_ID = "spotify:user:spotifycharts:playlist:0pZL6o5o9Rg4cPRyHBTPTN"
sp = spotipy.Spotify(
    auth_manager=SPOauth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public",
    )
)

# r = plc.find({})
# print(r[0])
# r = sp.playlist_add_items(PLAYLIST_ID, ["spotify:album:5SU0mrOWmwgMyEITPFFRBB"])
# print(r)
# playlist = {}
# results = sp.playlist_tracks(PLAYLIST_ID)["items"]
# for x in results:
#     playlist[f"{x['track']['artists'][0]['name']} - {x['track']['name']}"] = x["track"][
#         "uri"
#     ]
# for x in playlist:
#     data = {"name": x, "uri": playlist[x]}
#     r = plc.insert_one(data)
#     print(r.inserted_id)
# with open("playlist.json", "w") as f:
#    json.dump(results, f, indent=4)
# https://open.spotify.com/album/5SU0mrOWmwgMyEITPFFRBB?si=92z7f0zHR-qCnuwREm78zQ
# https://open.spotify.com/album/1i10no8p3y1igTW46jquub?si=LR1kyKmhQKi2l40ORzAgpg
# get album track
# album = sp.album(
#     "https://open.spotify.com/album/2FRA0dAkkapRAy7sH6c4yu?si=0ouPL3IARzegzfLovnisGA"
# )
# pprint(album)
# queued_uris = []
# for track in album["tracks"]["items"]:
#     queued_uris.append(track["uri"])
#     # print(track["name"], track["uri"])

# # get playlist tracks
# playlist_tracks = []
# playlist = sp.playlist_items(PLAYLIST_ID)["items"]
# for track in playlist:
#     playlist_tracks.append(track["track"]["uri"])

# # check for duplicates
# add_tracks = []
# for track in queued_uris:
#     if track not in playlist_tracks:
#         print(track)
#         add_tracks.append(track)

# # add tracks to playlist
# results = sp.playlist_add_items(PLAYLIST_ID, add_tracks)
# print(results)

track = sp.track(
    "https://open.spotify.com/track/7gvfh9IuHZe9j3SwLqY4qN?si=40acb3c120f64c84"
)

pprint(track)
