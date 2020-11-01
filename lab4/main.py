

from gevent.pywsgi import WSGIServer
from flask import Flask
app = Flask(__name__)



@app.route('/')
def index():
    return 'Hello, World! {7}'


http_server = WSGIServer(('127.0.0.1',8080), app)
http_server.serve_forever()


