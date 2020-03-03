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

        reverse_dict = {"tv": Show, "movie": Movie}

        self.known_for = [
            reverse_dict[r["media_type"]](self.client, r)
            for r in data.get("known_for", [])
        ]

        self._data = data

    def __repr__(self):
        return f"<Person name={self.name!r} id={self.id!r}>"

    # TODO - Expand


class Cast(Person):
    def __init__(self, item, data):
        self.item = item

        super().__init__(item.client, data)

        gender = data.get("gender")
        dictionary = {1: "Female", 2: "Male"}
        self.gender = dictionary.get(gender)
        self.character = data.get("character")
        self.credit_id = data.get("credit_id")
        self.order = data.get("order")
        self.cast_id = data.get("cast_id")

    # TODO - Expand + __repr__


class Crew(Person):
    def __init__(self, item, data):
        self.item = item

        super().__init__(item.client, data)

        gender = data.get("gender")
        dictionary = {1: "Female", 2: "Male"}
        self.gender = dictionary.get(gender)

        self.department = data.get("department")
        self.job = data.get("job")
        self.credit_id = data.get("credit_id")

    # TODO - Expand + __repr__
