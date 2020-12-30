from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Manager, Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import base64
from gevent.pywsgi import WSGIServer
from flask import Flask
from datetime import datetime
from models import User, Auditorium, Booking, app, db
import controllers
#from lab_4.data_base import app
#from data_base import User
#from lab_4.data_base import manager


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
auth = HTTPBasicAuth()


if __name__ =="__main__":
    import sys
    #manager.run()
    app.debug = True
    http_server = WSGIServer(('127.0.0.1', 8080), app)
    http_server.serve_forever()



