from .object import Object
from .util import date

class Season(Object):

    def __init__(self, show, data):
        self.show = show
        self.client = show.client

        self.episode_count = data.get("episode_count")
        self.id = data.get("id")
        self.name = data.get("name")
        self.overview = data.get("overview")
        self.poster = self.client.poster(data)
        self.season_number = data.get("season_number")
        rd = data.get("air_date")
        self.air_date = rd and date(rd)

        self._data = data
    
    def __repr__(self):
        return f"<Season name={self.name!r} season_number={self.season_number!r} id={self.id!r} show={self.show!r}>"
