import asyncio

from .http import HTTP
from .util import All
from .movie import Movie
from .show import Show
from .person import Person

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


    def urlmaker(self, type, url):
        if isinstance(url, dict):
            url = url.get(f"{type}_path")
        
        if not url: return

        base = self.config["secure_base_url"]
        size = self.config[f"{type}_sizes"][-2]

        return base+size+url


    def poster(self, url):
        return self.urlmaker("poster", url)
        
    def logo(self, url):
        return self.urlmaker("logo", url)
    
    def backdrop(self, url):
        return self.urlmaker("backdrop", url)

    def still(self, url):
        return self.urlmaker("still", url)
    
    def profile(self, url):
        return self.urlmaker("profile", url)

    async def search(self, query, *, cls=All, **params):
        dictionary = {
            Movie: "movie",
            Show: "tv",
            All: "multi",
            Person: "person"
        }

        reverse_dict = {
            "movie": Movie,
            "tv": Show,
            "person": Person
        }

        model = dictionary.get(cls)
        if not model:
            raise Exception #TODO - subclass
        
        params.update(query=query)

        data = await self.http.search(model, payload=params)

        data["query"] = params["query"]
        if cls == All:
            data["results"] = [
                reverse_dict[r["media_type"]](self, r)
                for r in data.get("results", [])
            ]
        else:
            data["results"] = [
                cls(self, r)
                for r in data.get("results", [])
            ]

        return data