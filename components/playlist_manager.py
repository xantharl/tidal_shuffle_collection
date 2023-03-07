import json
import tidalapi
from components.library_parser import LibraryParser
from connector.session_v2 import SessionV2


class PlaylistManager:
    def __init__(self, session: SessionV2) -> None:
        self._session: SessionV2 = session

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
            "countryCode": "US",
            "locale": "en_US"
            # "deviceType": "BROWSER",
        }

        # basic_request(self, method, path, params=None, data=None, headers=None)
        return self._session.request_v2.basic_request(
            "PUT", f"my-collection/playlists/folders/create-playlist", params=params
        )

        return response

    def get_lists_by_id(self, playlist_ids: list[str] = []):
        # params = {
        #     "includeOnly": "FAVORITE_PLAYLIST",
        #     "offset": "0",
        #     "limit": "50",
        #     "order": "DATE",
        #     "orderDirection": "DESC",
        #     "countryCode": "US",
        #     "locale": "en_US",
        #     "deviceType": "BROWSER",
        # }

        params = {
            "folderId": "root",
            "offset": "0",
            "limit": "50",
            "order": "DATE",
            "orderDirection": "DESC",
            "countryCode": "US",
            "locale": "en_US",
            "deviceType": "BROWSE",
        }

        path = "my-collection/playlists/folders/flattened"
        response = self._session.request_v2.basic_request("GET", path, params=params)
        if response.status_code != 200:
            raise Exception(f"Something went wrong! {response.reason}")

        return json.loads(response.content)

    def delete_list(self, playlist_id: str = None, playlist_name: str = None):
        if not playlist_id and not playlist_name:
            raise Exception(
                "PlaylistManager.delete_list: At least one of playlist_id or playlist_name must be provided"
            )

        path = "my-collection/playlists/folders/remove"

        params = {
            "trns": f"trn:playlist:{playlist_id}",
            "countryCode": "US",
            "locale": "en_US",
        }

        return self._session.request_v2.basic_request("PUT", path, params=params)

    def update_from_parser(self, parser: LibraryParser):
        pass

    def create_full_collection():
        pass
