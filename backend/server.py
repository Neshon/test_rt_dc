import asyncio

import tornado.web
import tornado.escape

from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body.decode('utf-8'))
        print('Got JSON data:', data)
        self.write({'got': 'your data'})


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
    asyncio.run(main())
