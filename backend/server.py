import asyncio

import tornado.web

from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


async def main():
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    print('ho')
    asyncio.run(main())
