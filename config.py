import os
from dotenv import load_dotenv

load_dotenv()

# Discord bot settings
discord_application_id = os.environ["discord_appid"]
discord_public_key = os.environ["discord_pubkey"]
discord_bot_name = "waffle"
discord_bot_token = os.environ["discord_token"]
discord_oauth_id = os.environ["discord_oauthid"]
discord_oauth_secret = os.environ["discord_oauth_secret"]
log_channel = os.environ["log_channel"]
dl_channel = os.environ["dl_channel"]
restart_role = os.environ["restart_role"]

# debrid settings
debrid_host = os.environ["debrid_host"]
debrid_key = os.environ["debrid_key"]
debrid_session = os.environ["debrid_session"]
http_url = os.environ["http_url"]
# dog api
dog_auth = os.environ["dog_auth"]
# cat api key
cat_auth = os.environ["cat_auth"]
# openai key
openai_key = os.environ["openai_key"]
# dbs
twitch_client_id = os.environ["twitch_client_id"]
twitch_secret = os.environ["twitch_secret"]
twitch_channel = os.environ["twitch_channel"]
twitch_notify_role = os.environ["twitch_notify_role"]

music_ip = os.environ["music_ip"]
emoji = "\N{WAFFLE}"
