from .object import Object

class Genre(Object):

    def __init__(self, client, data):
        self.client = client
        self.id = data.get("id")
        self.name = data.get("name")

    def __repr__(self):
        return f"<Genre name={self.name!r} id={self.id!r}>"
