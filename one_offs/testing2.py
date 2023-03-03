import requests
from connector import auth
from requests_oauth2 import OAuth2BearerToken
import tidalapi

auth_client = auth.Auth("session_data.json")
session: tidalapi.Session = auth_client.get_session()

# with requests.Session() as s:
#     s.auth = OAuth2BearerToken(session.access_token)
#     r = s.get("https://listen.tidal.com/my-collection/albums")
#     r.raise_for_status()
#     data = r.json()
# response = session.request.basic_request("GET", f"users/{session.user.id}/favorites" + "/artists").ok
favorites = tidalapi.Favorites(session, session.user.id)

artists: list[tidalapi.artist.Artist] = favorites.artists()
albums: list[tidalapi.album.Album] = favorites.albums()
album_ids: list[int] = [a.id for a in albums]
tracks: list[tidalapi.models.Track] = favorites.tracks()

# for artist in artists:
#     artist_albums = [album for album in artist.get_albums() if album.id not in


print(1)
