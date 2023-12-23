import logging
from contextlib import asynccontextmanager

import jobs
import tasks
from fastapi import FastAPI
from redis import Redis
from rq import Queue


logging.basicConfig(level=logging.DEBUG)

redis_conn = Redis(host="rq_redis")
flight_queue = Queue("flight_queue", connection=redis_conn)


@tasks.repeat_every(seconds=60)  # 1 minute
def check_flights():
    job = flight_queue.enqueue(jobs.check_flights)
    return {
        "job_id": job.id,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_flights()

    yield

    print("Shutting down...")


app = FastAPI(title="Flight Sleuth", version="0.1.0", lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Welcome to Flight Sleuth!"}
