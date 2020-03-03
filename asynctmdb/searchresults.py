from .object import Object


class SearchResults(Object):
    def __init__(self, client, data):
        self.client = client

        self.query = data.get("query")
        self.page = data.get("page")
        self.total_pages = data.get("total_pages")
        self.total_results = data.get("total_results")
        self.results = data.get("results")

        self._data = data

    def __repr__(self):
        return f"<SearchResults query={self.query!r}>"
