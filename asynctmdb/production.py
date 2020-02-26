from .object import Object

class Company(Object):

    def __init__(self, client, data):
        self.client = client
        self.name = data.get("name")
        self.id = data.get("id")
        self.logo = client.logo(data.get("logo_path"))
        self.country = data.get("origin_country")

    def __repr__(self):
        return f"<Company name={self.name!r} id={self.id!r}>"

class Country(Object):

    def __init__(self, client, data):
        self.client = client
        self.name = data.get("name")
        self.code = data.get("iso_639_1")

    def __repr__(self):
        return f"<Country name={self.name!r}>"

class Network(Object):
    
    def __init__(self, client, data):
        self.client = client
        self.name = data.get("name")
        self.id = data.get("id")
        self.logo = client.logo(data)
        self.country = data.get("origin_country")
    
    def __repr__(self):
        return f"<Network name={self.name!r} id={self.id!r}>"
    