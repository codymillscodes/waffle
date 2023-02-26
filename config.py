import os
from dotenv import load_dotenv

load_dotenv()

# convert to uppercase
# Discord bot settings
DISCORD_APPID = os.environ["discord_appid"]
DISCORD_PUBKEY = os.environ["discord_pubkey"]
BOT_NAME = "waffle"
BOT_TOKEN = os.environ["discord_token"]
DISCORD_OAUTH_ID = os.environ["discord_oauthid"]
DISCORD_OAUTH_SECRET = os.environ["discord_oauth_secret"]
LOG_CHANNEL = os.environ["log_channel"]
DL_CHANNEL = os.environ["dl_channel"]
RESTART_ROLE = os.environ["restart_role"]

# debrid settings
DEBRID_AGENT = os.environ["debrid_host"]
DEBRID_KEY = os.environ["debrid_key"]
DEBRID_SESSION = os.environ["debrid_session"]
DEBRID_WEBDAV = os.environ["http_url"]
# cat api key
CAT_KEY = os.environ["cat_auth"]
# openai key
OPENAI_KEY = os.environ["openai_key"]
# dbs
TWITCH_CLIENT_ID = os.environ["twitch_client_id"]
TWITCH_SECRET = os.environ["twitch_secret"]
TWITCH_CHANNEL = os.environ["twitch_channel"]
TWITCH_NOTIFY_ROLE = os.environ["twitch_notify_role"]
FORTNITE_API = os.environ["fortnite_api"]
#MUSIC_API = os.environ["music_ip"]
WAFFLE_EMOJI = "\N{WAFFLE}"
