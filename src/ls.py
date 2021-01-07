from fastapi.exceptions import HTTPException
from redis import Redis
from time import time
from random import randint
from re import compile

from config.config import redis_prefix

valid = compile(r"[a-zA-Z0-9_-]")


class IDGenerator:
    def __init__(self):
        self.increment = 0

    def next(self) -> str:
        t = round(time() * 1000) - 1608000000000
        if self.increment >= 2**5:
            self.increment = 0
        else:
            self.increment += 1
        return hex((t << 5) + self.increment + randint(0, 1000000))[2:]


class Shortener:
    def __init__(self):
        self.idg = IDGenerator()
        self.redis = Redis(host="redis")

    def create(self, longurl: str, short: str = None):
        if (not short) or not valid.match(short):
            short = self.idg.next()
        if self.redis.get(redis_prefix + short):
            raise HTTPException(400, "Duplicate short URL.")

        self.redis.set(redis_prefix + short, longurl)

        return {"status":"ok", "url":short}

    def get(self, short: str):
        if long := self.redis.get(redis_prefix + short):
            long = long.decode("utf-8")
            return long
        raise HTTPException(404, "Not found.")
