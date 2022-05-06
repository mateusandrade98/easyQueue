import os
from dotenv import dotenv_values


def getEnvData() -> dict:
    Env = dotenv_values(".env")
    if len(os.environ) > 0:
        Env.update(os.environ)
    return Env
