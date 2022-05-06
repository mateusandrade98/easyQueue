from util import getEnvironment
import redis

env = getEnvironment.getEnvData()


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
        from rq import Connection
        from rq import Worker as WorkerModule
        import sys

        with Connection():
            qs = sys.argv[1:] or ['default']
            w = WorkerModule(qs, connection=self.getConnection())
            w.work()
