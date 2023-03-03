class Album:
    def __init__(self, kwargs: dict):
        self._id = kwargs.get('id')
        self._tracks = kwargs.get('tracks')