import asyncio

from .http import HTTP

class Client:
    def __init__(self, *, api_key, loop=None, language="en-US", region="US"):
        self.api_key = api_key
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTP(self, loop=loop)
        self.language = language
        self.region = region

        self.config = {}
    
    def __repr__(self):
        return f"<Client language={self.language} region={self.region}>"
    
    async def _initialize(self):
        data = await self.http.get_config()
        self.config = data["images"]
