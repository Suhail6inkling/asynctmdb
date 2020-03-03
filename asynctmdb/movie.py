from .object import Object, AttributedDict
from .genre import Genre
from .person import Cast, Crew
from .production import Company, Country
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
        self.expanded = False

    def __repr__(self):
        return f"<Movie title={self.title!r} id={self.id!r} expanded={self.expanded!r}>"

    async def expand(self, *append):
        data = await self.client.http.get_movie(self.id, append)

        data.update(self._data)

        self.__init__(self.client, data)

        self.budget = data.get("budget")
        self.genres = [Genre(self.client, x) for x in data.get("genres", [])]
        self.production_companies = [
            Company(self.client, x) for x in data.get("production_companies")
        ]
        self.production_countries = [
            Country(self.client, x) for x in data.get("production_countries")
        ]
        self.tagline = data.get("tagline")
        self.status = data.get("status")
        self.runtime = data.get("runtime")
        self.revenue = data.get("revenue")

        self.expanded = True

        for a in append:
            subdata = data.get(a)
            if subdata:
                if a == "credits":
                    cast = [Cast(self, x) for x in subdata.get("cast")]
                    crew = [Crew(self, x) for x in subdata.get("crew")]
                    subdata["cast"] = cast
                    subdata["crew"] = crew

                    setattr(self, a, AttributedDict(**subdata))
                elif a == "changes":
                    subdata = subdata["changes"]
                    subdata = [
                        AttributedDict(key=v["key"], items=AttributedDict(**v["items"]))
                        for v in subdata
                    ]
                    setattr(self, a, subdata)
                # TODO - Similar Movies, Dates? Videos?
                elif len(subdata.keys()) == 1:
                    key = list(subdata.keys())[0]
                    value = subdata[key]
                    if isinstance(value, list):
                        subdata = [
                            AttributedDict(**a) if isinstance(a, dict) else a
                            for a in value
                        ]
                        setattr(self, a, subdata)
                    elif isinstance(value, dict):
                        setattr(self, a, AttributedDict(**value))
                    else:
                        setattr(self, a, subdata[key])
                else:
                    setattr(self, a, AttributedDict(**subdata))
