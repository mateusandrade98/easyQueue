class Request:
    def __init__(self):
        self.data = None

    async def run(self, data: dict = None):
        self.data = data
        if self.data:

            # modificar na library worker

            return {"success": 1}
