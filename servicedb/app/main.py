import asyncio
import logging
from contextlib import contextmanager

import aio_pika
from fastapi import FastAPI

from . import models, crud, schemas
from .database import engine, SessionLocal

app = FastAPI()

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

models.Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    asyncio.ensure_future(consume_appeal(loop))


async def insert_appeal(message: aio_pika.abc.AbstractIncomingMessage):
    logging.basicConfig(level=logging.DEBUG)
    async with message.process():
        appeal_s = schemas.AppealBase.parse_raw(message.body)
        logging.debug(f'Received message body: {appeal_s}')
        with get_db() as db:
            crud.create_appeal(db, appeal_s)


async def consume_appeal(loop):
    connection = await aio_pika.connect_robust(
        "amqp://admin:admin@rabbitmq/",
        loop=loop
    )

    queue_name = "task_queue"
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(insert_appeal)
    try:
        await asyncio.Future()
    finally:
        await connection.close()


@app.get('/appeal/')
async def appeal():
    with get_db() as db:
        return crud.get_appeal(db)
