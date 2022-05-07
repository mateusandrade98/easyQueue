import requests


class Request:
    def __init__(self):
        self.data = None

    async def run(self, data: dict = None):
        self.data = data
        if self.data:
            url = self.data["url"]

            exit()

            if "redirect" in self.data:
                requests.post(
                    url=url,
                    json=self.data
                )

                return {"success": 1}

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

            requests.request(
                method=method,
                url=url,
                headers=headers,
                data=payload,
                params=params
            )

            return {"success": 1}
