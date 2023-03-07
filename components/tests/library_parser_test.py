import unittest
from components.library_parser import LibraryParser
import tidalapi
from connector.auth import Auth


class LibraryParserTest(unittest.TestCase):
    def setup(self):
        self._auth = Auth("session_data.json")
        self._session = self._auth._init_session()
        self._favorites = tidalapi.Favorites(self._session, self._session.user.id)

    def test_parse_tracks(self):
        self.setup()
        parser = LibraryParser(self._favorites)
        parser._parse_tracks()

        # This test will fail for users with > 30 tracks favorited for any one artist
        #   but I don't have that many favorited and just want to do a rudimentary test
        self.assertEqual(len(self._favorites.tracks()), len(parser.all_tracks))

    def test_parse_collection(self):
        self.setup()
        pass

    def test_parse_artists(self):
        self.setup()
        pass


if __name__ == "__main__":
    unittest.main()
