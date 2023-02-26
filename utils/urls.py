from enum import Enum
import config

class Urls(Enum):
    # debrid urls
    DEBRID_BASE_URL = 'https://api.alldebrid.com/v4/'
    DEBRID_CRED = f'agent={config.api_host}&apikey={config.api_key}'
    DEBRID_HOSTS = f'{DEBRID_BASE_URL}hosts?{DEBRID_CRED}'
    DEBRID_PING = f'{DEBRID_BASE_URL}ping?{DEBRID_CRED}'
    DEBRID_STATUS = f'{DEBRID_BASE_URL}magnet/status?{DEBRID_CRED}'
    DEBRID_STATUS_READY = f'{DEBRID_STATUS}&status=ready'
    DEBRID_STATUS_ACTIVE = f'{DEBRID_STATUS}&status=active'
    DEBRID_STATUS_ONE = f'{DEBRID_BASE_URL}magnet/status?{DEBRID_CRED}&id='
    DEBRID_DELETE = f'{DEBRID_BASE_URL}magnet/delete?{DEBRID_CRED}&id='
    DEBRID_RESTART = f'{DEBRID_BASE_URL}magnet/restart?{DEBRID_CRED}&id='
    DEBRID_UPLOAD = f'{DEBRID_BASE_URL}magnet/upload?{DEBRID_CRED}&magnets[]='
    DEBRID_INSTANT = f'{DEBRID_BASE_URL}magnet/instant?{DEBRID_CRED}&magnets[]='
    DEBRID_INFOS = f'{DEBRID_BASE_URL}link/infos?{DEBRID_CRED}&link='
    DEBRID_UNLOCK = f'{DEBRID_BASE_URL}link/unlock?{DEBRID_CRED}&link='
    DEBRID_STREAMING = f'{DEBRID_BASE_URL}link/streaming?{DEBRID_CRED}&stream='
    DEBRID_DELAYED = f'{DEBRID_BASE_URL}link/delayed?{DEBRID_CRED}&id='
    # cat urls
    CAT_BASE_URL = 'https://api.thecatapi.com/v1/'
    CAT_RANDOM = f'{CAT_BASE_URL}images/search?api_key={config.cat_api_key}'
    CAT_GIF = f'{CAT_BASE_URL}images/search?mime_types=gif&api_key={config.cat_api_key}'
    CAT_NEB = f'{CAT_BASE_URL}images/search?breed_ids=nebe&api_key={config.cat_api_key}'
    # runescape urls
    RUNESCAPE3_HISCORE = 'https://secure.runescape.com/m=hiscore/index_lite.ws?player='
    # waffle urls
    WAFFLE_URL = 'https://randomwaffle.gbs.fm/'
    # misc urls
    TWITCH_URL = 'https://api.twitch.tv/helix/streams?user_login='