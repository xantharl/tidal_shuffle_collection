import copy
from datetime import datetime
import json
import os
from pathlib import Path
import tidalapi

from connector.session_v2 import SessionV2


class Auth:
    def __init__(self, session_data_file: Path = None):
        self._session_data_file = session_data_file
        self._init_config()
        self._init_session()

    def _init_session(self) -> None:
        if not self._session_data_file or not os.path.exists(self._session_data_file):
            self._create_new_session()
        else:
            self._session = SessionV2(session_data=self._config)

    @property
    def session(self):
        return self._session

    def _create_new_session(self):
        session = SessionV2()
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
        self._session = session

    def _init_config(self):
        with open(self._session_data_file, "r") as session_data:
            self._config = json.loads(session_data.read())
            self._config["expiry_time"] = datetime.strptime(
                self._config["expiry_time"], "%Y-%m-%d %H:%M:%S.%f"
            )
