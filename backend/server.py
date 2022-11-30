import asyncio
import json
import logging
import os
from time import sleep

import aio_pika
import tornado.escape
import tornado.web
from aio_pika.message import Message
from tornado.options import define, options, parse_command_line


RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
QUEUE_NAME = os.environ['QUEUE_NAME']

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

logger = logging.getLogger(__name__)


# Подключения к RabbitMQ, если не доступно, то повторяет операцию
async def connect_rabbitmq():
    rabbitmq_connection = None

    while not rabbitmq_connection:
        rabbitmq_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"
        try:
            rabbitmq_connection = await aio_pika.connect_robust(rabbitmq_url)
            logger.info("Connect to rabbitmq.")
        except Exception:
            logger.info("Can't connect to rabbitmq.")
            sleep(5)

    return rabbitmq_connection


# Отправка сообщений в очередь
class AppealRequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    async def post(self) -> None:
        connection = self.application.settings["amqp_connection"]
        channel = await connection.channel()
        data = tornado.escape.json_decode(self.request.body.decode('utf-8'))
        queue = await channel.declare_queue(name=QUEUE_NAME, durable=True)
        try:
            await channel.default_exchange.publish(
                Message(
                    body=json.dumps(data).encode(),
                    content_type="application/json",
                ),
                routing_key=queue.name
            )
            logger.info(f"Send message: {data}")
        finally:
            await channel.close()


async def make_app() -> tornado.web.Application:
    amqp_connection = await connect_rabbitmq()
    # Ручка для фронта
    return tornado.web.Application(
        [(r"/appeal", AppealRequestHandler)],
        amqp_connection=amqp_connection,
    )


async def main():
    parse_command_line()
    app = await make_app()
    app.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
