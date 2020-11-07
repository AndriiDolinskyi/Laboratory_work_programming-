# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from gevent.pywsgi import WSGIServer
from flask import Flask
app = Flask(__name__)



@app.route('/')
def index():
    return 'Hello, World! {7}'
# Press the green button in the gutter to run the script.

http_server = WSGIServer(("127.0.0.1", 8080), app)
http_server.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
