from .object import Object, AttributedDict
from .genre import Genre
from .person import Person, Cast, Crew
from .production import Company, Country, Network
from .season import Season
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
        self.expanded = False
    
    def __repr__(self):
        return f"<Show name={self.name!r} id={self.id!r} expanded={self.expanded!r}>"
    
    async def expand(self, *append):
        data = await self.client.http.get_show(self.id, append)

        data.update(self._data)

        self.__init__(self.client, data)

        self.created_by = [Person(self.client, x) for x in data.get("created_by")]
        self.genres = [Genre(self.client, x) for x in data.get("genres", [])]
        self.production_companies = [Company(self.client, x) for x in data.get("production_companies")]
        self.networks = [Network(self.client, x) for x in data.get("networks")]
        self.tagline = data.get("tagline")
        self.status = data.get("status")

        rd = data.get("last_air_date")
        self.last_air_date = rd and date(rd)

        self.season_count = data.get("number_of_seasons")
        self.episode_count = data.get("number_of_episodes")

        self.seasons = [Season(self, x) for x in data.get("seasons")]

        self.expanded = True

        for a in append:
            subdata = data.get(a)
            if subdata:
                if a == "credits":
                    cast = [
                        Cast(self, x)
                        for x in subdata.get("cast")
                    ]
                    crew = [
                        Crew(self, x)
                        for x in subdata.get("crew")
                    ]
                    subdata["cast"] = cast
                    subdata["crew"] = crew

                    setattr(self, a, AttributedDict(**subdata))
                elif a == "changes":
                    subdata = subdata["changes"]
                    subdata = [AttributedDict(
                        key=v["key"],
                        items=AttributedDict(**v["items"])
                    ) for v in subdata]
                    setattr(self, a, subdata)
                elif a == "keywords":
                    subdata = subdata["keywords"]
                    subdata = [
                        AttributedDict(**v)
                        for v in subdata
                    ]
                    setattr(self, a, subdata)
                #TODO - Similar Shows, Dates? Videos?
                elif len(subdata.keys()) == 1:
                    key = list(subdata.keys())[0]
                    setattr(self, a, subdata[key])
                else:
                    setattr(self, a, AttributedDict(**subdata))
