import json
import requests
from connector import auth
from requests_oauth2 import OAuth2BearerToken
import tidalapi

auth_client = auth.Auth("session_data.json")
session: tidalapi.Session = auth_client._init_session()
session.config.api_location = session.config.api_location.replace("v1", "v2")
session.config.item_limit = 50

response = session.request.basic_request(
    "GET", f"my-collection/playlists/folders/flattened"
)
# favorites = tidalapi.Favorites(session, session.user.id)
# https://listen.tidal.com/v2/my-collection/playlists/folders/create-playlist?description=&folderId=root&isPublic=false&name=tester&countryCode=US&locale=en_US&deviceType=BROWSER
# https://listen.tidal.com/v2/favorites/mixes/ids?limit=500&cursor=&countryCode=US&locale=en_US&deviceType=BROWSER

# artists: list[tidalapi.artist.Artist] = favorites.artists()
# logged_in_user = tidalapi.LoggedInUser(session, session.user.id)
# lists: list[tidalapi.Playlist] = logged_in_user.playlists()

print(json.dumps(json.loads(response.text), indent=4))
