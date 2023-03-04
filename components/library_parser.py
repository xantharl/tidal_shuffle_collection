import logging
import tidalapi
from config.config import Config


class LibraryParser:
    def __init__(self, favorites: tidalapi.Favorites) -> None:
        self._favorites = favorites
        self._all_tracks: "dict[int, list[tidalapi.Track]]" = {}
        self._config = Config.instance().data
        self._artist_max = self._config.get("playlist_maximums").get(
            "tracks_per_artist", 100000
        )

    @property
    def all_tracks(self) -> list[tidalapi.Track]:
        if not self._all_tracks:
            self._parse()

        data = []
        for tracks in self._all_tracks.values():
            data.extend(tracks)

        return data

    @property
    def track_ids(self) -> list[int]:
        return [t.id for t in self._all_tracks]

    def artist_count(self, lookup_artist_id: tidalapi.Artist) -> int:
        artist_tracks = [
            tracks
            for artist_id, tracks in self._all_tracks.items()
            if artist_id == lookup_artist_id
        ]
        return len(artist_tracks) if artist_tracks else 0

    def artist_limit(self, artist_id: tidalapi.Artist) -> int:
        return self._artist_max - self.artist_count(artist_id)

    def _parse(self):
        self._parse_tracks()
        self._parse_albums()
        self._parse_artists()

    def _parse_tracks(self):
        # self._all_tracks = self._favorites.tracks()
        all_tracks: list[tidalapi.Track] = self._favorites.tracks()
        artist_ids = set([track.artist.id for track in all_tracks])
        for artist_id in artist_ids:
            tracks = [track for track in all_tracks if track.artist.id == artist_id]

            if artist_id not in self._all_tracks:
                self._all_tracks[artist_id] = []

            self._all_tracks[artist_id].extend(
                tracks[: self.artist_limit(artist_id) - 1]
            )

    def _parse_albums(self):
        albums: list[tidalapi.album.Album] = self._favorites.albums()
        albums_by_artist: "dict[int, list[tidalapi.Track]]" = {}
        for album in albums:
            if album.artist.id not in albums_by_artist:
                albums_by_artist[album.artist.id] = []

            albums_by_artist[album.artist.id].extend(album)

        for artist_id, albums in albums_by_artist.items():
            limit = self.artist_limit(artist_id)
            if limit <= 0:
                continue

            for album in albums:
                if limit <= 0:
                    continue

                tracks = album.tracks(limit=limit)
                limit -= len(tracks)

                if artist_id not in self._all_tracks:
                    self._all_tracks[artist_id] = []

                self._all_tracks[artist_id].extend(tracks)

    def _parse_artists(self):
        top_track_limit = self._config.get("favorite_artists").get("top_tracks", 10000)
        if top_track_limit <= 0:
            logging.info(
                f"favorite_artists.top_tracks is <= 0, no tracks added for favorite artists."
            )
            return

        artists: list[tidalapi.artist.Artist] = self._favorites.artists()
        for artist in artists:
            limit = min(self.artist_limit(artist.id), top_track_limit)
            tracks = artist.get_top_tracks(limit)

            if artist not in self._all_tracks:
                self._all_tracks[artist] = []

            self._all_tracks[artist].extend(tracks)
