from tidalapi.session import Session, Config

from connector.requests_v2 import RequestsV2


class SessionV2(Session):
    def __init__(self, config=Config(), session_data: dict = None):
        super().__init__(config)
        self.load_existing_session(session_data)
        self.request_v2 = RequestsV2(session=self)

    def load_existing_session(self, config: dict):
        if not self.load_oauth_session(**config):
            raise Exception(
                f"Failed to load existing session from {self._session_data_file}"
            )
