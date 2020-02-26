from .object import Object


class Person(Object):

    def __init__(self, client, data):
        self.client = client
    
        self.name = data.get("name")
        self.id = data.get("id")
        self.profile = client.profile(data)
        self.popularity = data.get("popularity")

        from .show import Show
        from .movie import Movie

        reverse_dict = {
            "tv": Show,
            "movie": Movie
        }

        self.known_for = [
            reverse_dict[r["media_type"]](self.client, r)
            for r in data.get("known_for", [])
        ]

        self._data = data

    def __repr__(self):
        return f"<Person name={self.name!r} id={self.id!r}>"

