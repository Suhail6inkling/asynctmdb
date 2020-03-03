from .object import Object
from .person import Cast, Crew


class Episode(Object):
    def __init__(self, season, data):
        self.season = season
        self.show = season.show
        self.client = season.client

        self.name = data.get("name")
        self.id = data.get("id")
        self.overview = data.get("overview")
        self.episode_number = data.get("episode_number")
        self.production_code = data.get("production_code")
        self.still = self.client.still(data)

        self.crew = [Crew(self, x) for x in data.get("crew")]

        self.guest_stars = [Cast(self, x) for x in data.get("crew")]

        self._data = data

    def __repr__(self):
        return f"<Episode name={self.name!r} episode_number={self.episode_number!r} id={self.id!r} season={self.season!r}>"
