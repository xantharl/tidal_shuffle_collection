import json
import logging
import tidalapi
from components.library_parser import LibraryParser
from connector.session_v2 import SessionV2


class PlaylistManager:
    """
    Extension class for the default tidalapi which supports the V2 API routes.
    V1 appears to only expose *some* playlists, I cannot determine how it decides which to provide.
    """

    def __init__(self, session: SessionV2) -> None:
        self._session: SessionV2 = session
        self._refresh_playlists()

    @property
    def playlists(self):
        return self._playlists

    def _refresh_playlists(self):
        self._playlists = self.get_playlists()

    def create_list(
        self,
        playlist_name: str = "My Collection",
        description: str = "The entire collection!",
    ):
        params = {
            "description": description,
            "folderId": "root",
            "isPublic": "false",
            "name": f"{playlist_name}",
        }

        # basic_request(self, method, path, params=None, data=None, headers=None)
        response = self._session.request_v2.basic_request(
            "PUT", f"my-collection/playlists/folders/create-playlist", params=params
        )

        self._playlists.append(
            tidalapi.Playlist(self._session, None).parse(
                json.loads(response.text).get("data")
            )
        )
        return self._playlists[-1]

    def get_playlists(self):
        params = {
            "folderId": "root",
            "offset": "0",
            "limit": "50",
            "order": "DATE",
            "orderDirection": "DESC",
        }

        path = "my-collection/playlists/folders/flattened"
        response = self._session.request_v2.basic_request("GET", path, params=params)
        if response.status_code != 200:
            raise Exception(f"Something went wrong! {response.reason}")

        items = json.loads(response.content).get("items")
        playlists: list[tidalapi.Playlist] = []
        for item in items:
            data = item.get("data")
            if data and data.get("uuid"):
                playlists.append(tidalapi.Playlist(self._session, None).parse(data))

        return playlists

    def delete_playlist(self, playlist: tidalapi.Playlist):
        path = "my-collection/playlists/folders/remove"

        params = {
            "trns": f"trn:playlist:{playlist.id}",
            "countryCode": "US",
            "locale": "en_US",
        }

        response = self._session.request_v2.basic_request("PUT", path, params=params)
        if 204 != response.status_code:
            logging.error(f"Failed to delete list {playlist.name}")
            logging.error(f"Response: {json.dumps(response)}")
        else:
            self._playlists.remove(playlist)

        return response

    def add_tracks_to_playlist(
        self, playlist: tidalapi.Playlist, tracks: list[tidalapi.Track]
    ):
        pass

    def update_from_parser(self, parser: LibraryParser):
        pass

    def create_full_collection():
        pass
