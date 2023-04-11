import aiohttp
from loguru import logger


class Connection:
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def get_json(self, url, headers=None, data=None):
        try:
            if headers is None:
                headers = {}
            if data is None:
                data = {}
            async with self.session.get(
                url, headers=headers, data=data, timeout=self.timeout
            ) as resp:
                return await resp.json()
        except TimeoutError:
            logger.info("Timeout error")
            return None
        except:
            logger.info(resp.text)
            return None

    async def get_text(self, url):
        async with self.session.get(url, timeout=self.timeout) as resp:
            return await resp.text()

    async def read(self, url):
        async with self.session.get(url, timeout=self.timeout) as resp:
            return await resp.read()

    async def get(self, url):
        async with self.session.get(url, timeout=self.timeout) as resp:
            return await resp

    async def post_json(self, url, headers=None, data=None):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        async with self.session.post(
            url, headers=headers, data=data, timeout=self.timeout
        ) as resp:
            return await resp.json()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
