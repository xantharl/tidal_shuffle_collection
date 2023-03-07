import logging
import unittest
from components.library_parser import LibraryParser
import tidalapi
from connector.auth import Auth


class LibraryParserTest(unittest.TestCase):
    def setup(self):
        self._auth = Auth("session_data.json")
        self._session = self._auth.session
        self._favorites = tidalapi.Favorites(self._session, self._session.user.id)
        return LibraryParser(self._favorites)

    def test_parse_tracks(self):
        parser = self.setup()
        parser._parse_tracks()

        # This test will fail for users with > 30 tracks favorited for any one artist
        #   but I don't have that many favorited and just want to do a rudimentary test
        self.assertEqual(len(self._favorites.tracks()), len(parser.all_tracks))

    def test_parse_collection(self):
        parser = self.setup()
        track_count = len(parser.all_tracks)
        print(track_count)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    unittest.main()
