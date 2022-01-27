import json
import threading
import redis
from rq import Queue
from rq import Retry
import Sender
from util import getEnvironment
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify

env = getEnvironment.getEnvData()

app = Flask(__name__)
app.debug = True


def error(msg=str) -> jsonify:
    return jsonify({
        "success": 0,
        "msg": msg
    })


def success(data=dict):
    return jsonify({
        "success": 1,
        "data": data
    })


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


@app.route("/test")
def test():
    return success({"result": "ok"})


@app.route("/addToQueue", methods=["POST", "GET"])
def addToQueue():
    if request.method != "POST":
        return error("This method is invalid.")

    if not request.json:
        return error("Send JSON type data.")

    try:
        if request.args["token"] != env.get("token"):
            return error("Token is invalid.")
    except KeyError as e:
        return error("KeyError {e}".format(e=e))

    try:
        data = request.json
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


def startHttpServer():
    print("HTTP Server Started...")
    httpserver = WSGIServer((
        env.get("service_host"),
        int(env.get("service_port"))), app)
    httpserver.serve_forever()


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
    http_server = WSGIServer((
        env.get("service_host"),
        int(env.get("service_port"))),
        app
    )
    threading.Thread(target=startHttpServer, args=()).start()
    startWorkerServer()
