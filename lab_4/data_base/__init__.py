from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Manager, Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:and3010@127.0.0.1/lab_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True,  nullable=False)
    password = db.Column(db.String(70),nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Auditorium(db.Model):
    __tablename__ = "auditoriums"
    id = db.Column(db.Integer, primary_key=True)
    number_of_auditorium = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, number):
        self.number_of_auditorium = number

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"), nullable=False)
    auditorium_id = db.Column(db.Integer, db.ForeignKey(Auditorium.id, ondelete="cascade"), nullable=False)
    booking_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    expire_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, auditorium_id, booking_date_time, expire_date_time):
        self.user_id = user_id
        self.auditorium_id = auditorium_id
        self.booking_date_time = booking_date_time
        self.expire_date_time = expire_date_time





@app.route('/')
def index():

    return 'Hello, World!'+ '  Some data has been added to DB'

@app.route("/api/v1/hello-world-/<num_of_variant>")
def hello_world(num_of_variant):
    #user = User("Andrii", "exp@smth.com", "123456")
    #aud = Auditorium(1)
    d1 = datetime(2017, 3, 5, 12, 30, 10)
    d2 = datetime(2017, 3, 6, 12, 30, 10)
    booking = Booking(6, 4, d1, d2)
    #db.session.add(user)
    #db.session.add(aud)
    db.session.add(booking)
    db.session.commit()
    return 'Hello, World! {'+ num_of_variant + '}'

# app.debug = True
# http_server = WSGIServer(('127.0.0.1',8080), app)
# http_server.serve_forever()

