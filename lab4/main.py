from gevent.pywsgi import WSGIServer
from flask import Flask

app = Flask(__name__)



@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/api/v1/hello-world-/<num_of_variant>")
def hello_world(num_of_variant):
    return 'Hello, World! {'+ num_of_variant + '}'

app.debug = True
http_server = WSGIServer(('127.0.0.1',8080), app)
http_server.serve_forever()