import url
import config
import requests


def get_link_info(link, agent, api_key):
    c = requests.get(
        url.create(
            "infos",
            link=link,
            agent=agent,
            api_key=api_key,
        )
    )

    return c.json()
