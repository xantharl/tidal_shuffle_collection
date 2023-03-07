from components.playlist_manager import PlaylistManager
import unittest

from connector.auth import Auth


class PlaylistManagerTest(unittest.TestCase):
    def setup(self):
        self._auth = Auth("session_data.json")
        return PlaylistManager(session=self._auth.session)

    def test_get_lists(self):
        manager = self.setup()
        lists = manager.get_lists_by_id()
        print(1)

    def test_create_list(self):
        manager = self.setup()
        # list = manager.create_list()


if __name__ == "__main__":
    unittest.main()
