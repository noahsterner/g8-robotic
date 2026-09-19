# file: src/http/http_client.py

import requests
import logging

logger = logging.getLogger(__name__)

class HttpClient:
    def __init__(self, base_url: str, timeout: float = 7.0):
        self._base_url: str = base_url.rstrip("/")
        self._timeout: float = timeout

    def get(self, endpoint: str):
        return self._request("GET", endpoint)
        
    def post(self, endpoint: str, data: dict):
        return self._request("POST", endpoint, data)

    def put(self, endpoint: str, data: dict):
        return self._request("PUT", endpoint, data)

    def delete(self, endpoint: str):
        return self._request("DELETE", endpoint)

    def _request(self, method: str, endpoint: str, data: dict | None = None):
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        logger.info("Sending %s request to: %s", method, url)

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                timeout=self._timeout
            )

            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()

        except requests.exceptions.RequestException as error:
            logger.error("%s request failed: %s", method, error)
            raise
