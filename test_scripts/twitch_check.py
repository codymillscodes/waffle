from twitchAPI.twitch import Twitch
import asyncio
toauth = "cshs9kb6ije9bxyf478wmnqrzmfzmn"
async def twitch_example(auth):
    # initialize the twitch instance, this will by default also create a app authentication for you

    # twitch = await Twitch('d793pdsta85foxl7reb8ytrqqo2ywy', toauth)
    users = ["punchlordtv", "exafterdark", "codemiko"]
    online = []

    async for s in Twitch.get_streams(auth, user_login=["punchlordtv", "exafterdark", "CodeMiko", "PirateSoftware"]):
        if s.user_login in users:
            print(s.user_login + " online.")
        online.append(s.user_login)

    print(online)
twitch = Twitch('d793pdsta85foxl7reb8ytrqqo2ywy', toauth)
# run this example
asyncio.run(twitch_example(twitch))