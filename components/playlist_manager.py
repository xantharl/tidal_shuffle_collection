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
        response = self._session.request_v2.basic_request(
            "PUT", f"my-collection/playlists/folders/create-playlist", params=params
        )

        return response

    def get_lists_by_id(self, playlist_ids: list[str]):
        pass

    def delete_list(self, playlist_id: str = None, playlist_name: str = None):
        if not playlist_id and not playlist_name:
            raise Exception(
                "PlaylistManager.delete_list: At least one of playlist_id or playlist_name must be provided"
            )

    def update_from_parser(self, parser: LibraryParser):
        pass

    def create_full_collection():
        pass
