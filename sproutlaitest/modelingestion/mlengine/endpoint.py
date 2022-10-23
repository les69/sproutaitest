import json
from typing import Dict

import requests

from modelingestion.interfaces.exceptions import ApiEndpointException
from modelingestion.interfaces.mlendpoint import LanguageDetectionModelProtocol
from modelingestion.request.models import MLEndpointResponse


class DetectionModelEndpoint(LanguageDetectionModelProtocol):
    protocol_name = "detection_model_endpoint"

    _DEFAULT_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, rest_endpoint: str, headers: Dict[str, str] = None) -> None:
        super().__init__()
        self._endpoint = rest_endpoint
        self._headers = headers or self._DEFAULT_HEADERS

    def detect_foul_language_in_sentence(self, sentence: str) -> bool:
        """
        Call a REST Api where a ML model will detect if the sentence contains any foul language
        :param sentence:
        :return:
        """
        response = requests.post(url=self._endpoint, data=json.dumps({"fragment": sentence.lower()}),
                                 headers=self._headers)
        if response.status_code != 200:
            raise ApiEndpointException(f"Endpoint returned unsuccessful status code {response.status_code}")
        response = MLEndpointResponse.build_from_endpoint_response(payload=response.json())
        return response.has_foul_language
