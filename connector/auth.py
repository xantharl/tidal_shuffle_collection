from datetime import datetime
import json
import os
from pathlib import Path
import tidalapi


class Auth:
    def __init__(self, session_data_file: Path = None):
        self._session_data_file = session_data_file

    def get_session(self) -> tidalapi.Session:
        if not self._session_data_file or not os.path.exists(self._session_data_file):
            return self._get_new_session()
        else:
            return self._load_existing_session()

    def _get_new_session(self):
        session = tidalapi.Session()
        # Will run until you visit the printed url and link your account
        session.login_oauth_simple()
        with open(self._session_data_file, "w+") as session_data:
            config = {
                "access_token": session.access_token,
                "expiry_time": str(session.expiry_time),
                "refresh_token": session.refresh_token,
                "token_type": session.token_type,
            }
            session_data.write(json.dumps(config))
        return session

    def _load_existing_session(self):
        with open(self._session_data_file, "r") as session_data:
            config = json.loads(session_data.read())
            config["expiry_time"] = datetime.strptime(
                config["expiry_time"], "%Y-%m-%d %H:%M:%S.%f"
            )
            session = tidalapi.Session()
            if not session.load_oauth_session(**config):
                raise Exception(
                    f"Failed to load existing session from {self._session_data_file}"
                )
        return session
