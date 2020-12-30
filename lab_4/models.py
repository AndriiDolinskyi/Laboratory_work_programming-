from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Response
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:and3010@127.0.0.1/lab_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
