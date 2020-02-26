import asyncio
import aiohttp


class Request:
    base = "https://api.themoviedb.org/3"

    def __init__(self, method, endpoint, **kwargs):
        self.method = method

        self.params = kwargs.pop("params", {})
        self.data = kwargs.pop("data", None)
        self.json = kwargs.pop("json", None)
        self.headers = kwargs.pop("headers", None)

        if endpoint:
            endpoint = endpoint.lstrip("/")
            self.url = f"{self.base}/{endpoint}"

    @property
    def kwargs(self):
        return dict(
            params=self.params, data=self.data, json=self.json, headers=self.headers
        )


class HTTP:
    def __init__(self, client, *, session=None, loop=None):
        self.client = client
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession()
        self.locale = None

    @property
    def api_key(self):
        return self.client.api_key
    
    @property
    def region(self):
        return self.client.region
    
    @property
    def language(self):
        return self.client.language

    @staticmethod
    def append_dict(append):
        return {
            "append_to_response": (
                ",".join(append)
            )
        }

    async def request(self, req, override = False):
        if not self.client.config and not override:
            await self.client._initialize()
        req.params.update(
            api_key=self.api_key,
            region=self.region,
            language=self.language
        )

        async with self.session.request(req.method, req.url, **req.kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            resp.raise_for_status()
    
    async def get_config(self):
        return await self.request(Request("GET", "configuration"), override=True)

    async def search(self, model, payload):
        return await self.request(Request("GET", f"search/{model}", params=payload))
    
    async def get_movie(self, id, append):
        return await self.request(Request("GET", f"movie/{id}", params=self.append_dict(append)))
    
    async def get_show(self, id, append):
        return await self.request(Request("GET", f"tv/{id}", params=self.append_dict(append)))
    
    async def get_season(self, tvid, snum, append):
        return await self.request(Request("GET", f"tv/{tvid}/season/{snum}", params=self.append_dict(append)))
