from components.playlist_manager import PlaylistManager
import unittest
import tidalapi

from connector.auth import Auth
from requests import Response


class PlaylistManagerTest(unittest.TestCase):
    def setup(self):
        self._auth = Auth("session_data.json")
        return PlaylistManager(session=self._auth.session)

    def test_get_lists(self):
        manager = self.setup()
        lists = manager.get_playlists()
        self.assertIsInstance(lists[0], tidalapi.UserPlaylist)

    def test_list_crud(self):
        manager = self.setup()
        title = "unit test list"
        descr = "it's a description"
        test_list = manager.create_list(title, descr)

        self.assertIsInstance(test_list, tidalapi.UserPlaylist)
        self.assertEqual(title, test_list.name)
        self.assertEqual(descr, test_list.description)
        self.assertIn(test_list, manager.playlists)

        never_gonna_give_you_up = tidalapi.Track(self._auth.session, "177186841")
        bananaphone = tidalapi.Track(self._auth.session, "35503648")
        tracks = [never_gonna_give_you_up, bananaphone]

        manager.add_tracks_to_playlist(test_list, tracks)
        remote_tracks_ids = [t.id for t in test_list.tracks()]
        self.assertEqual(len(remote_tracks_ids), len(tracks))

        # Comparing the full object fails equality check, so we're settling for IDs
        self.assertIn(never_gonna_give_you_up.id, remote_tracks_ids)
        self.assertIn(bananaphone.id, remote_tracks_ids)

        result = manager.delete_playlist(test_list)
        self.assertEqual(result.status_code, 204)
        self.assertNotIn(
            test_list,
            manager.playlists,
            f"UserPlaylist '{test_list.name}' is still present in lists.",
        )


if __name__ == "__main__":
    unittest.main()
