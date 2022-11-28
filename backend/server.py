import asyncio
import json
import logging
from time import sleep

import aio_pika
import tornado.escape
import tornado.web
from aio_pika.message import Message
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


async def connect_rabbitmq():
    rabbitmq_connection = None
    rabbitmq_chanel = None

    while not rabbitmq_connection:
        conn_str = "amqp://admin:admin@rabbitmq/"
        try:
            rabbitmq_connection = await aio_pika.connect_robust(conn_str)
        except Exception as e:
            print("Can't connect to broker.")
            sleep(5)

    if not rabbitmq_chanel:
        rabbitmq_chanel = await rabbitmq_connection.channel()

    return rabbitmq_chanel


class AppealRequestHandler(tornado.web.RequestHandler):
    logging.basicConfig(level=logging.DEBUG)

    async def post(self):
        data = tornado.escape.json_decode(self.request.body.decode('utf-8'))
        logging.debug(f'Received message body: {data}')
        print('Got JSON data:', data)

        channel = await connect_rabbitmq()
        queue = await channel.declare_queue(name='task_queue', durable=True)
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(data).encode(),
                content_type="application/json",
            ),
            routing_key=queue.name
        )


def make_app():
    return tornado.web.Application([
        ('/appeal', AppealRequestHandler)
    ])


async def main():
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
