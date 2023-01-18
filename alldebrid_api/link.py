import url
import config
import requests

api = config.api_key
agent = config.agent


def get_link_info(link):
    c = requests.get(url.create(agent, api, "infos", link))

    return c.json()


print(get_link_info("https://www.youtube.com/watch?v=21T-Sc-TXJY")["data"])
