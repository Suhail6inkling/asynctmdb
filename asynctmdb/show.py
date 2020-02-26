from .object import Object
from .util import date

class Show(Object):
    def __init__(self, client, data):
        self.client = client

        self.id = data.get("id")
        self.name = data.get("name")
        self.genre_ids = data.get("genre_ids")
        self.overview = data.get("overview")
        rd = data.get("first_air_date")
        self.first_air_date = rd and date(rd)
        self.poster = client.poster(data)
        self.backdrop = client.backdrop(data)

        self.popularity = data.get("popularity")

        self._data = data
    
    def __repr__(self):
        return f"<Show name={self.name!r} id={self.id!r}>"
    
