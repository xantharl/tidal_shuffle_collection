import json
import os
import requests
import tidalapi
from requests_oauth2 import OAuth2BearerToken
from datetime import datetime

session_data_file = 'session_data.json'

if not os.path.exists(session_data_file):
    session = tidalapi.Session()
    # Will run until you visit the printed url and link your account
    session.login_oauth_simple()
    with open (session_data_file, 'w+') as session_data:
        config = {
            'access_token': session.access_token,
            'expiry_time' : str(session.expiry_time),
            'refresh_token' : session.refresh_token,
            'token_type' : session.token_type
        }
        session_data.write(json.dumps(config))
else:
    with open(session_data_file, 'r') as session_data:
        config = json.loads(session_data.read())
        config['expiry_time'] = datetime.strptime(config['expiry_time'], '%Y-%m-%d %H:%M:%S.%f')
        session = tidalapi.Session()
        if not session.load_oauth_session(**config):
            raise Exception(f"Failed to load existing session from {session_data_file}")

# # albums = session.page.get("pages/my_collection_albums")
# with requests.Session() as s:
#     s.auth = OAuth2BearerToken(session.access_token)
#     r = s.get("https://listen.tidal.com/my-collection/albums")
#     r.raise_for_status()
#     data = r.json()

album = session.album(66236918)
tracks = album.tracks()
for track in tracks:
    print(track.name)