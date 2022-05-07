import requests
import json


class Request:
    def __init__(self):
        self.data = None

    async def run(self, data: dict = None):
        self.data = data
        if self.data:
            url = self.data["url"]

            if "redirect" in self.data:
                response = requests.post(
                    url=url,
                    json=self.data
                )

                try:
                    return await response.json()
                except json.JSONDecodeError:
                    return response.text

            try:
                payload = self.data["payload"]
            except KeyError:
                payload = {}

            try:
                headers = self.data["headers"]
                values_headers = headers.items()
                headers = {str(key): str(value) for key, value in values_headers}  # convert key:value to string
            except KeyError:
                headers = {}

            try:
                method = self.data["method"]
            except KeyError:
                method = "GET"

            try:
                params = self.data["params"]
            except KeyError:
                params = {}

            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=payload,
                params=params
            )

            try:
                return await response.json()
            except json.JSONDecodeError:
                return response.text
