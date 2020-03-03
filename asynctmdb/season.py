from .object import Object
from .util import date
from .episode import Episode


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

        self.expanded = False
        self._data = data

    def __repr__(self):
        return f"<Season name={self.name!r} season_number={self.season_number!r} id={self.id!r} show={self.show!r} expanded={self.expanded!r}>"

    async def expand(self, *append):

        data = await self.client.http.get_season(
            self.show.id, self.season_number, append
        )

        data.update(self._data)

        self.__init__(self.show, data)

        self.episodes = [Episode(self, x) for x in data.get("episodes")]

        self.expanded = True
