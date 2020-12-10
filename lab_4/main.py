
from sqlalchemy import create_engine
from gevent.pywsgi import WSGIServer
from flask import Flask
from data_base import app
#from data_base import User
from data_base import manager

if __name__ =="__main__":
    import sys
    #manager.run()
    app.debug = True
    http_server = WSGIServer(('127.0.0.1', 8080), app)
    http_server.serve_forever()


# app = Flask(__name__)
#
#
#
# @app.route('/')
# def index():
#     return 'Hello, World!'
#
# @app.route("/api/v1/hello-world-/<num_of_variant>")
# def hello_world(num_of_variant):
#     return 'Hello, World! {'+ num_of_variant + '}'
#
# app.debug = True
# http_server = WSGIServer(('127.0.0.1',8080), app)
# http_server.serve_forever()
