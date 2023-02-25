# https://docs.alldebrid.com
from bot import Waffle


def create(
    request, link="", magnet="", magnetid="", agent="", api_key="", stream="", id=""
):
    base_url = "https://api.alldebrid.com/v4/"
    cred = f"agent={agent}&apikey={api_key}"

    if link != "":
        if request in {"infos", "unlock", "streaming", "delayed"}:
            if request == "streaming":
                return f"{base_url}link/{request}?{cred}&id={id}&stream={stream}"
            if request == "delayed":
                return f"{base_url}link/{request}?{cred}&id={id}"
            return f"{base_url}link/{request}?{cred}&link={link}"
        return "request must be infos, unlock, streaming or delayed"
    if magnetid != "":
        if request in {"status", "delete", "restart"}:
            return f"{base_url}magnet/{request}?{cred}&id={magnetid}"
        return "request must be status, delete or restart"
    if magnet != "":
        if request in {"upload", "instant"}:
            return f"{base_url}magnet/{request}?{cred}&magnets[]={magnet}"
        return "request must be upload or instant"
    elif request == "status":
        return f"{base_url}magnet/{request}?{cred}&status=active"
    elif request == "ready":
        return f"{base_url}magnet/status?{cred}&status=ready"
    elif request == "all":
        return f"{base_url}magnet/status?{cred}"
    elif request == "ping":
        return f"{base_url}ping?agent={agent}"
    elif request == "hosts":
        return f"{base_url}hosts?agent={agent}"


async def upload_magnet(magnet, agent, api_key, bot: Waffle):
    try:
        async with bot.session.get(
            create("upload", magnet=magnet, agent=agent, api_key=api_key),
            timeout=30,
        ) as resp:
            r = await resp.json()
        magnet_info = [
            r["data"]["magnets"][0]["id"],
            r["data"]["magnets"][0]["name"],
            r["data"]["magnets"][0]["ready"],
        ]
        return magnet_info
    except KeyError:
        print(r)
        return r["error"]["message"]


async def get_all_magnet_status(agent, api_key, bot: Waffle):
    async with bot.session.get(create("status", agent=agent, api_key=api_key)) as resp:
        r = await resp.json()
    if len(r["data"]["magnets"]) <= 0:
        return 0
    else:
        return r["data"]["magnets"]


async def get_magnet_status(magnetid, agent, api_key, bot: Waffle):
    try:
        async with bot.session.get(
            create("status", magnetid=magnetid, agent=agent, api_key=api_key)
        ) as resp:
            r = await resp.json()
        return r["data"]["magnets"]["status"]
    except KeyError:
        return r["error"]["message"]


async def delete_magnet(magnetid, agent, api_key, bot: Waffle):
    try:
        async with bot.session.get(
            create("delete", magnetid=magnetid, agent=agent, api_key=api_key)
        ) as resp:
            r = await resp.json()
        return r["data"]["message"]
    except KeyError:
        return r["error"]["message"]


def restart_magnet(magnetid):
    pass


async def instant_magnet(magnet, agent, api_key, bot: Waffle):
    async with bot.session.get(
        create("instant", magnet=magnet, agent=agent, api_key=api_key)
    ) as resp:
        r = await resp.json()
    return r["data"]["magnets"][0]["instant"]


apiErrors = {
    "GENERIC": "An error occured",
    "404": "Endpoint doesn't exist",
    "AUTH_MISSING_AGENT": "You must send a meaningful agent parameter, see api docs",
    "AUTH_BAD_AGENT": "Bad agent",
    "AUTH_MISSING_APIKEY": "The auth apikey was not sent",
    "AUTH_BAD_APIKEY": "The auth apikey is invalid",
    "AUTH_BLOCKED": "This apikey is geo-blocked or ip-blocked",
    "AUTH_USER_BANNED": "This account is banned",
    "LINK_IS_MISSING": "No link was sent",
    "LINK_HOST_NOT_SUPPORTED": "This host or link is not supported",
    "LINK_DOWN": "This link is not available on the file hoster website",
    "LINK_PASS_PROTECTED": "Link is password protected",
    "LINK_HOST_UNAVAILABLE": "Host under maintenance or not available",
    "LINK_TOO_MANY_DOWNLOADS": "Too many concurrent downloads for this host",
    "LINK_HOST_FULL": "All servers are full for this host, please retry later",
    "LINK_HOST_LIMIT_REACHED": "You have reached the download limit for this host",
    "LINK_ERROR": "Could not unlock this link",
    "REDIRECTOR_NOT_SUPPORTED": "Redirector not supported",
    "REDIRECTOR_ERROR": "Could not extract links",
    "STREAM_INVALID_GEN_ID": "Invalid generation ID",
    "STREAM_INVALID_STREAM_ID": "Invalid stream ID",
    "DELAYED_INVALID_ID": "This delayed link id is invalid",
    "FREE_TRIAL_LIMIT_REACHED": "You have reached the free trial limit (7 days // 25GB downloaded or host uneligible for free trial)",
    "MUST_BE_PREMIUM": "You must be premium to process this link",
    "MAGNET_INVALID_ID": "This magnet ID does not exists or is invalid",
    "MAGNET_INVALID_URI": "Magnet is not valid",
    "MAGNET_INVALID_FILE": "File is not a valid torrent",
    "MAGNET_FILE_UPLOAD_FAILED": "File upload failed",
    "MAGNET_NO_URI": "No magnet sent",
    "MAGNET_PROCESSING": "Magnet is processing or completed",
    "MAGNET_TOO_MANY_ACTIVE": "Already have maximum allowed active magnets (30)",
    "MAGNET_MUST_BE_PREMIUM": "You must be premium to use this feature",
    "MAGNET_NO_SERVER": "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.",
    "MAGNET_TOO_LARGE": "Magnet files are too large (max 1TB)",
    "PIN_ALREADY_AUTHED": "You already have a valid auth apikey",
    "PIN_EXPIRED": "The pin is expired",
    "PIN_INVALID": "The pin is invalid",
    "USER_LINK_MISSING": "No link provided",
    "USER_LINK_INVALID": "Can't save those links",
    "NO_SERVER": "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.",
    "MISSING_NOTIF_ENDPOINT": "You must provide an endpoint to unsubscribe",
    "VOUCHER_DURATION_INVALID": "Invalid voucher duration (must be either 15, 30, 90, 180 or 365)",
    "VOUCHER_NB_INVALID": "Invalid voucher number, must be between 1 and 10",
    "NO_MORE_VOUCHER": "No voucher of this type available in your account",
    "INSUFFICIENT_BALANCE": "Your current reseller balance is not enough to generate the requested vouchers",
}
