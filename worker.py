from util import getWorker

def startServer():
    worker = getWorker.Worker()
    from rq import Connection
    from rq import Worker as WorkerModule
    import sys

    with Connection():
        qs = sys.argv[1:] or ['default']
        w = WorkerModule(qs, connection=worker.getConnection())
        w.work()


if __name__ == "__main__":
    print("Worker Server Started...")
    startServer()