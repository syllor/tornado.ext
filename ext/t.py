import os

import tornado.options
from tornado.options import options
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import web
from tornado import gen
import redis
from session import *
from db import SQLAlchemy

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


db = SQLAlchemy("sqlite:///aa.db")

class User(db.Model):
    username = Column(String(16), unique=True, nullable=False)
    password = Column(String(30), nullable=False)


class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            ('/', bbbHandler)
        ]
        settings = dict(
            debug = True,
            autoescape = None,
            cookie_secret = 'secret',
            xsrf_cookies = False,

        )
        tornado.web.Application.__init__(self, handlers, **settings)
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.redis = redis.Redis(connection_pool=pool)
        self.session_store = RedisSessionStore(self.redis)  
 
class BaseHandler(tornado.web.RequestHandler):
 
    def get_current_user(self):
        return self.session['user'] if self.session and 'user' in self.session else None

    @property
    def session(self):
        sessionid =self.get_secure_cookie('sid')
        return Session(self.application.session_store,sessionid)

class bbbHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('sid','1') 
       # self.session['user'] = ['1','2']
       # print self.session['user'] 
        u = User(username='xxa3',password="bb")
        db.session.add(u)
        db.session.commit()
       # db.create_db()
       # user = User.query.
       # print user
          
        self.write("xxx")


def run_server():
    tornado.options.parse_command_line()
    Application().listen(8000)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    run_server()
