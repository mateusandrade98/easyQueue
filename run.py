from datetime import timedelta
from rq import Queue, Retry
from util import getEnvironment, getWorker
from fastapi import FastAPI, Request
import Sender
import uvicorn
import json

env = getEnvironment.getEnvData()

app = FastAPI()
app.debug = True


def error(msg: str = "") -> json:
    return {
        "success": 0,
        "msg": msg
    }


def success(data: dict = "") -> json:
    return {
        "success": 1,
        "data": data
    }


@app.post("/addToQueue")
async def addToQueue(request: Request, token: str = ""):
    if not request.json:
        return error("Send JSON type data.")

    try:
        if token != env.get("token"):
            return error("Token is invalid.")
    except KeyError as e:
        return error("KeyError {e}".format(e=e))

    try:
        data = await request.json()
    except json.JSONDecoder as e:
        return error("JSONDecodeError {e}".format(e=e))

    delay = 0
    if "delay" in data:
        delay = float(data["delay"])

    worker = getWorker.Worker()
    q = Queue(connection=worker.getConnection())
    q.enqueue_at(
        timedelta(seconds=delay),
        Sender.Request().run,
        data,
        retry=Retry(max=3, interval=[10, 30, 60])
    )
    return success({"Sender.Request": data})

if __name__ == "__main__":
    print("HTTP Server Started...")
    uvicorn.run(
        app,
        host=env.get("service_host"),
        port=int(env.get("service_port"))
    )

