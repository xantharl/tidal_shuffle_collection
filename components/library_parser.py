import logging
import tidalapi
from config.config import Config
from domain.artist_behavior import ArtistBehavior


class LibraryParser:
    def __init__(self, favorites: tidalapi.Favorites) -> None:
        self._favorites = favorites
        self._all_tracks: list[tidalapi.Track] = None

    @property
    def all_tracks(self):
        if not self._all_tracks:
            self._parse()

        return self._all_tracks

    @property
    def track_ids(self) -> list[int]:
        return [t.id for t in self._all_tracks]

    def artist_count(self, artist) -> int:
        artist_tracks = [t for t in self._all_tracks if t.artist.id == artist.id]
        return len(artist_tracks) if artist_tracks else 0

    def _parse(self):
        self._parse_tracks()
        self._parse_albums()
        self._parse_artists()

        max_per_artist = Config.instance().data.get("max_per_artist")
        if max_per_artist:
            self._prune_artists(max_per_artist)

    def _parse_tracks(self):
        self._all_tracks = self._favorites.tracks()

    def _parse_albums(self):
        data = Config.instance().data
        artist_max = data.get("max_per_artist", 50)
        # TODO: Implement collision resolution and max
        albums: list[tidalapi.album.Album] = self._favorites.albums()
        for album in albums:
            self._all_tracks.extend(
                [t for t in album.tracks if t.id not in self.track_ids]
            )

    def _parse_artists(self, artist_behavior: ArtistBehavior):
        data = Config.instance().data
        artist_behavior = data.get("artist_behavior", ArtistBehavior.TOPX)
        if artist_behavior == ArtistBehavior.NONE:
            logging.info("Artist Behavior is set to NONE, skipping artist...")

        artists: list[tidalapi.artist.Artist] = self._favorites.artists()
        artist_max = data.get("max_per_artist", 50)

        if artist_behavior == ArtistBehavior.TOPX:
            for artist in artists:
                limit = artist_max - self.artist_count(artist)
                self._all_tracks.extend(artist.get_top_tracks(limit=limit))
        else:  # ArtistBehavior.ALL is the only remaining option
            for artist in artists:
                for album in artist.get_albums():
                    limit = artist_max - self.artist_count(artist)
                    if limit <= 0:
                        break
                    album.tracks(limit=limit)

    def _prune_artists(self, max_per_artist):
        pass
