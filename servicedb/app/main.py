import asyncio
import logging
import os
from contextlib import contextmanager
from time import sleep

import aio_pika
from fastapi import FastAPI

from .crud import create_appeal
from .database import engine, SessionLocal
from .models import Base
from .schemas import AppealSchema

RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
QUEUE_NAME = os.environ['QUEUE_NAME']


app = FastAPI()

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Подключения к RabbitMQ, если не доступно, то повторяет операцию
async def connect_rabbitmq(loop):
    rabbitmq_connection = None

    while not rabbitmq_connection:
        rabbitmq_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"
        try:
            rabbitmq_connection = await aio_pika.connect_robust(
                url=rabbitmq_url,
                loop=loop
            )
            logging.info("Connect to rabbitmq.")
        except Exception:
            logging.info("Can't connect to rabbitmq.")
            sleep(5)

    return rabbitmq_connection


# Валидация данных и вызов функции сохранения
async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        appeal_s = AppealSchema.parse_raw(message.body)
        logging.info(f'Received message: {appeal_s}')
        with get_db() as db:
            create_appeal(db, appeal_s)


# Получение сообщений из очереди
async def consume_appeal(loop):
    connection = await connect_rabbitmq(loop)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    await queue.consume(process_message)
    try:
        await asyncio.Future()
    finally:
        await connection.close()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    asyncio.ensure_future(consume_appeal(loop))
