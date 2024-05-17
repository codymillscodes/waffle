import requests
import streamrip

url = "http://192.168.1.238/api/station/wafflefm/requests?="
request_url = "http://192.168.1.238/api/station/wafflefm/request/"
##### search for a song that DOES exist
# get request_id
# r = requests.get(url + "miss+murder").json()
# print(r[0]["request_id"])

##### search for a song that doesnt exist
# r = requests.get(url + "taylor+swift").json()
# print(r)
# returns []

##### search and request a song that exists
r = requests.get(url + "").json()
print(r)
# req = requests.post(request_url + r[0]["request_id"]).json()
# print(req)

##### search and download album from deezer
# arl = "d5866819a7ea9f0a6b9ed99ecfac7dcb3b1b011672f6169ab78f6ee91ac3f058961210ed45595f619b0eab63215d1dae0b78b2925159b1ea86b85ab49c6ce39a06b8e95e9ed0d1d8c277641ab331bac4ee9cb5b7abfeb411eb6aed5dc6baa050"
# deezer = streamrip.clients.DeezerClient()
# deezer.login(arl=arl)
# search = deezer.search("deafheaven dream house")

# album_id = search["data"][0]["id"]

# album = streamrip.media.Album(client=deezer, id=album_id)
# album.load_meta()
# album.download(quality=0, parent_folder=search["data"][0]["artist"]["name"])
##### search for track
# artist name, album title
# search = deezer.search("deafheaven dream house", media_type="track")
# track = streamrip.media.Track(
#    client=deezer,
#     id=search["data"][0]["id"],
# )

# track.load_meta()
# track.download(
#     parent_folder=f"{search['data'][0]['artist']['name']}",
#     add_singles_to_folder=True,
#     quality=0,
# )
