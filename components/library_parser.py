import logging
import requests
import tidalapi
from config.config import Config


class LibraryParser:
    def __init__(
        self,
        favorites: tidalapi.Favorites,
        album_cache_enabled: bool = True,
        track_limit: int = None,
    ) -> None:
        self._favorites = favorites
        self._all_tracks: "dict[int, list[tidalapi.Track]]" = {}
        self._track_limit = track_limit
        self._all_track_count: int = 0
        self._config = Config.instance().data
        self._artist_max = self._config.get("playlist_maximums").get(
            "tracks_per_artist", 100000
        )
        self._album_cache_enabled = album_cache_enabled

    @property
    def all_tracks(self) -> list[tidalapi.Track]:
        if not self._all_tracks:
            self._parse()

        data = []
        for tracks in self._all_tracks.values():
            data.extend(tracks)

        return data

    @property
    def playlists(self) -> list[tidalapi.Playlist]:
        return self._favorites.playlists()

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

    @property
    def track_capacity(self) -> int:
        if not self._track_limit:
            return 9999999
        else:
            return self._track_limit - self._all_track_count

    def artist_limit(self, artist_id: tidalapi.Artist) -> int:
        return min(self._artist_max, self.track_capacity) - self.artist_count(artist_id)

    def _parse(self):
        self._parse_tracks()
        self._parse_albums()
        self._parse_artists()

    def _parse_tracks(self):
        all_tracks: list[tidalapi.Track] = self._favorites.tracks()
        artist_ids = set([track.artist.id for track in all_tracks])
        for artist_id in artist_ids:
            tracks = [track for track in all_tracks if track.artist.id == artist_id]

            if artist_id not in self._all_tracks:
                self._all_tracks[artist_id] = []

            to_add = tracks[: self.artist_limit(artist_id) - 1]
            self._all_track_count += len(to_add)
            self._all_tracks[artist_id].extend(to_add)

    def _parse_albums(self):
        albums: list[tidalapi.album.Album] = self._favorites.albums()
        albums_by_artist: "dict[int, list[tidalapi.Track]]" = {}
        for album in albums:
            if album.artist.id not in albums_by_artist:
                albums_by_artist[album.artist.id] = []

            albums_by_artist[album.artist.id].append(album)

        for artist_id, albums in albums_by_artist.items():
            limit = self.artist_limit(artist_id)
            if limit <= 0:
                continue

            for album in albums:
                if limit <= 0:
                    continue

                try:
                    tracks = album.tracks(limit=limit)
                    logging.info(
                        f"Successfully fetched album {album.artist.name} - {album.name}"
                    )
                except requests.exceptions.HTTPError as e:
                    logging.warning(
                        f"HTTP Error for Album {album.artist.name} - {album.name}"
                    )
                    logging.warning(e)

                limit -= len(tracks)
                self._all_track_count += len(tracks)

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
            if limit <= 0 and self.track_capacity <= 0:
                break

            tracks = artist.get_top_tracks(limit)
            self._all_track_count += len(tracks)

            if artist not in self._all_tracks:
                self._all_tracks[artist] = []

            self._all_tracks[artist].extend(tracks)

    # def _album_cache_lookup(self, album: tidalapi.Album):
    #     if not hasattr(self, "_album_cache"):
    #         self._init_album_cache()

    #     matches = [a for a in self._album_cache if a == album]
    #     if matches:
    #         return matches[0]
    #     else:
    #         return None

    # def _init_album_cache(self):
    #     cache_file = f"cache/{self.session.user.id}_album_cache.json"
    #     with open(cache_file, "r") as cache_stream:
    #         cache_data = cache_stream.read()

    #     self._album_cache = [
    #         tidalapi.Album(None, None).parse(album_json) for album_json in cache_data
    #     ]
