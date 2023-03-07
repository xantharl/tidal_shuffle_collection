import copy
from tidalapi.request import Requests


class RequestsV2(Requests):
    common_params = {"countryCode": "US", "locale": "en_US"}

    def __init__(self, session):
        super().__init__(session)
        self.session = copy.deepcopy(session)
        self.session.config.api_location = self.session.config.api_location.replace(
            "v1", "v2"
        )

    def basic_request(self, method, path, params: dict = None, data=None, headers=None):
        params.update(RequestsV2.common_params)
        return super().basic_request(method, path, params, data, headers)
