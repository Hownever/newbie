# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'jj'
__mtime__ = '2017/11/14'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/Login', permanent=True)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')


class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


if __name__ == "__main__":
    isdebug = True
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/Login", LoginHandler),
            (r"/Regist", RegistHandler),
            (r"/Index", IndexHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=isdebug
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()