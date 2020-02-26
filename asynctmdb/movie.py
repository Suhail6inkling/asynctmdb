from .object import Object
from .util import date

class Movie(Object):
    def __init__(self, client, data):
        self.client = client

        self.id = data.get("id")
        self.title = data.get("title")
        self.genre_ids = data.get("genre_ids")
        self.adult = data.get("adult")
        self.overview = data.get("overview")
        rd = data.get("release_date")
        self.release_date = rd and date(rd)
        
        self.poster = client.poster(data)
        self.backdrop = client.backdrop(data)

        self.popularity = data.get("popularity")

        self._data = data
    
    def __repr__(self):
        return f"<Movie title={self.title!r} id={self.id!r}>"
    
