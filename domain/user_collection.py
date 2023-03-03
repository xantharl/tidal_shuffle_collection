from domain.album import Album

class UserCollection:
    def __init__(self, albums: list[Album]):
        self._albums = albums