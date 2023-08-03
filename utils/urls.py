from enum import StrEnum
import config


class Urls(StrEnum):
    # debrid urls
    DEBRID_BASE_URL = "https://api.alldebrid.com/v4/"
    DEBRID_CRED = f"agent={config.DEBRID_AGENT}&apikey={config.DEBRID_KEY}"
    DEBRID_HOSTS = f"{DEBRID_BASE_URL}hosts?{DEBRID_CRED}"
    DEBRID_PING = f"{DEBRID_BASE_URL}ping?{DEBRID_CRED}"
    DEBRID_STATUS = f"{DEBRID_BASE_URL}magnet/status?{DEBRID_CRED}"
    DEBRID_STATUS_READY = f"{DEBRID_STATUS}&status=ready"
    DEBRID_STATUS_ACTIVE = f"{DEBRID_STATUS}&status=active"
    DEBRID_STATUS_ONE = f"{DEBRID_BASE_URL}magnet/status?{DEBRID_CRED}&id="
    DEBRID_DELETE = f"{DEBRID_BASE_URL}magnet/delete?{DEBRID_CRED}&id="
    DEBRID_RESTART = f"{DEBRID_BASE_URL}magnet/restart?{DEBRID_CRED}&id="
    DEBRID_UPLOAD = f"{DEBRID_BASE_URL}magnet/upload?{DEBRID_CRED}&magnets[]="
    DEBRID_INSTANT = f"{DEBRID_BASE_URL}magnet/instant?{DEBRID_CRED}&magnets[]="
    DEBRID_INFOS = f"{DEBRID_BASE_URL}link/infos?{DEBRID_CRED}&link="
    DEBRID_UNLOCK = f"{DEBRID_BASE_URL}link/unlock?{DEBRID_CRED}&link="
    DEBRID_STREAMING = f"{DEBRID_BASE_URL}link/streaming?{DEBRID_CRED}&id="
    DEBRID_DELAYED = f"{DEBRID_BASE_URL}link/delayed?{DEBRID_CRED}&id="
    # cat urls
    CAT_BASE_URL = "https://api.thecatapi.com/v1/"
    CAT_RANDOM = f"{CAT_BASE_URL}images/search?api_key={config.CAT_KEY}"
    CAT_GIF = f"{CAT_BASE_URL}images/search?mime_types=gif&api_key={config.CAT_KEY}"
    CAT_NEB = f"{CAT_BASE_URL}images/search?breed_ids=nebe&api_key={config.CAT_KEY}"
    # runescape urls
    RUNESCAPE3_HISCORE = "https://secure.runescape.com/m=hiscore/index_lite.ws?player="
    # waffle urls
    WAFFLE_URL = "https://randomwaffle.gbs.fm/"
    # misc urls
    TWITCH_URL = "https://api.twitch.tv/helix/streams?user_login="
    TWITCH_CHANNEL = "https://www.twitch.tv/"
    TWITCH_TOKEN_REQUEST = "https://id.twitch.tv/oauth2/token"
    # azura


class Azura(StrEnum):
    IP = config.AZURA_IP
    STATION = config.AZURA_STATION_ID
    STATION_URL = f"{IP}/station/{STATION}"
    GET_API_STATUS = f"{IP}/status"
    GET_CPU_STATS = f"{IP}/admin/server/stats"

    GET_STATION_STATUS = f"{STATION_URL}/status"
    RESTART_STATION = f"{STATION_URL}/restart"

    GET_NOW_PLAYING = f"{IP}/nowplaying/{STATION}"
    GET_REQUESTS = f"{STATION_URL}/requests"
    SEND_REQUEST = f"{STATION_URL}/request/"
    GET_PLAYBACK_HISTORY = f"{STATION_URL}/history"
    GET_LISTENERS = f"{STATION_URL}/listeners"
    GET_QUEUE = f"{STATION_URL}/queue"
    DELETE_QUEUE_ITEM = f"{STATION_URL}/"
    SEND_FILE = f"{STATION_URL}/files"
    # add custom field urls
