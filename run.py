import json
import redis
from rq import Queue
from rq import Retry
import Sender
from util import getEnvironment
from fastapi import FastAPI, Request

env = getEnvironment.getEnvData()

app = FastAPI()
app.debug = True


def error(msg=str) -> json:
    return {
        "success": 0,
        "msg": msg
    }


def success(data=dict) -> json:
    return {
        "success": 1,
        "data": data
    }


class Worker:
    def __init__(self):
        pass

    def getConnection(self):
        return redis.client.Redis(
            host=env.get("redis_host"),
            port=env.get("redis_port"),
            db=env.get("redis_db"),
            password=env.get("redis_password")
        )

    def start(self):
        print("Wpp Worker Started....")
        worker = Worker()
        from rq import Connection
        from rq import Worker as WorkerModule
        import sys

        with Connection():
            qs = sys.argv[1:] or ['default']
            w = WorkerModule(qs, connection=worker.getConnection())
            w.work()


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

    worker = Worker()
    q = Queue(connection=worker.getConnection())
    q.enqueue(
        Sender.Request().run,
        data,
        retry=Retry(max=3, interval=[10, 30, 60])
    )
    return success({"Sender.Request": data})


def startServer():
    print("HTTP Server Started...")
    startWorkerServer()
    import uvicorn
    uvicorn.run(
        "run:app",
        host=env.get("service_host"),
        port=int(env.get("service_port")),
        log_level="info"
    )


def startWorkerServer():
    print("Worker Started....")
    worker = Worker()
    from rq import Connection
    from rq import Worker as WorkerModule
    import sys

    with Connection():
        qs = sys.argv[1:] or ['default']
        w = WorkerModule(qs, connection=worker.getConnection())
        w.work()


if __name__ == "__main__":
    print("Server Started...")
    startServer()
