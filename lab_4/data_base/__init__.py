from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Manager, Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import base64
#from lab_4.controllers.schemas import user_schema

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:and3010@127.0.0.1/lab_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
auth = HTTPBasicAuth()


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


bcrypt = Bcrypt(app)
ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')

class AuditoriumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'number_of_auditorium')

class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'auditorium_id', 'booking_date_time', 'expire_date_time')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
auditorium_schema = AuditoriumSchema()
auditoriums_schema = AuditoriumSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)



def datetime_validation(aud_id, d, e):
    all_bookings = Booking.query.all()
    for booking in all_bookings:
        if booking.auditorium_id == int(aud_id):
            d1 = datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
            d2 = datetime.strptime(e,"%Y-%m-%dT%H:%M:%S")
            # print(str(d1) + "----" + str(d2))

            #print(type(d1))
            #ds = datetime.strptime(booking.booking_date_time,"%Y-%m-%dT%H:%M:%S")
            ds = booking.booking_date_time
            #print(type(ds))
            #df = datetime.strptime(booking.expire_date_time,"%Y-%m-%dT%H:%M:%S")
            df = booking.expire_date_time
            # print(str(ds) + "----" + str(df))
            # print(ds <= d1 <= df)
            # print(ds <= d2 <= df)
            # print(ds == d1)
            if ds <= d1 <= df:
                print("in between")
                return False
            elif ds <= d2 <= df:
                print("in between")
                return False
            else:
                continue


    return True

def check(authorization_header):
    all_user =  User.query.all()
    #version2
    [basic, encoded_uname_pass] = authorization_header.split()
    print(encoded_uname_pass)
    encoded_uname_pass = base64.b64decode(encoded_uname_pass).decode()
    [name, password] = encoded_uname_pass.split(':')

    for user in all_user:

        # if encoded_uname_pass == base64.b64encode(str(user.name + ":" + user.password).encode("ascii")).decode("ascii"):
        #     return True
        if name == user.name and  bcrypt.check_password_hash(user.password, password):
            return True

    return False

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            resp.data = "You need to be logged in to do this"
            return resp, 401
        return f(*args, **kwargs)
    return decorated


@app.route("/api/v1/hello-world-/<num_of_variant>")
def hello_world(num_of_variant):

      return 'Hello, World! {'+ num_of_variant + '}'


@app.route('/login', methods=['GET'])
def login():

    all_users = User.query.all()



    authorization_header = request.headers.get("Authorization")
    [basic, encoded_uname_pass] = authorization_header.split()
    print(encoded_uname_pass)
    encoded_uname_pass = base64.b64decode(encoded_uname_pass).decode()
    [name, password] = encoded_uname_pass.split(':')
    print(name)
    print(password)
    for user in all_users:
        print(bcrypt.generate_password_hash(password))
        print(user.password)
        if user.name == name and bcrypt.check_password_hash(user.password, password):
            basic = str(name) + ':' + str(user.password)
            print(type(basic))
            basic = basic.encode("ascii")
            basic = base64.b64encode(basic)
            basic = basic.decode("ascii")

            resp = Response()
            resp.headers["Basic"] = basic
            resp.data = "You are logged in"
            return resp

    return "Invalid name or password", 404


#User methods
@app.route('/user/register', methods=['POST'])
def add_user():
    def valid_body_message():
         return jsonify(["Invalid body!, Valid body: ", {"name": "string", "email": "string", "password": "string"}]), 400

    all_users = User.query.all()

    req_data = request.get_json()
    name= None
    email = None
    password = None

    if 'name' in req_data:
         name = req_data['name']
    else:
        return valid_body_message()

    if 'email' in req_data:
         email = req_data['email']
    else:
        return valid_body_message()

    if 'password' in req_data:
         password = req_data['password']
    else:
        return valid_body_message()





    password = bcrypt.generate_password_hash(password)

    for user in all_users:
        if user.email == email:
            return "User with such email already exists", 409

    new_user = User(name, email, password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):

    user = User.query.get(user_id)
    if user == None:
        return "User not found", 404

    return user_schema.jsonify(user)


#Auditorium methods

@app.route('/auditorium', methods=['POST'])
@login_required
def add_auditorium():
    all_auditoriums = Auditorium.query.all()

    req_data = request.get_json()
    number = None

    if 'number_of_auditorium' in req_data:
        number = req_data['number_of_auditorium']
    else:
        return jsonify(["Invalid body! Valid body:", {"number_of_auditorium": "int"}]), 400

    for aud in all_auditoriums:
        if aud.number_of_auditorium == number:
            return "Auditorium with such number already exists", 409

    new_auditorium = Auditorium(number)
    db.session.add(new_auditorium)
    db.session.commit()

    return auditorium_schema.jsonify(new_auditorium), 201

@app.route('/auditorium', methods=['GET'])
def get_auditoriums():
    all_auditoriums = Auditorium.query.all()
    result = auditoriums_schema.dump(all_auditoriums)
    return jsonify(result)

@app.route('/auditorium/<auditorium_id>', methods=['GET'])
def get_auditorium(auditorium_id):
    auditorium = Auditorium.query.get(auditorium_id)
    if auditorium == None:
        return "Auditorium not found", 404

    return auditorium_schema.jsonify(auditorium)


#Booking methods
@app.route('/booking', methods=['POST'])
@login_required
def add_booking():
    def valid_body_message():
        return jsonify(["Invalid body!, Valid body: ", {"user_id": "int", "auditorium_id": "int", "booking_date_time": "datetime", "expire_date_time": "datetime"}]), 400

    req_data = request.get_json()

    user_id = None
    auditorium_id = None
    booking_date_time = None
    expire_date_time = None

    if 'user_id' in req_data:
        user_id = req_data['user_id']
    else:
        return valid_body_message()
    if 'auditorium_id' in req_data:
        auditorium_id = req_data['auditorium_id']
    else:
        return valid_body_message()
    if 'booking_date_time' in req_data:
        booking_date_time = req_data['booking_date_time']
    else:
        return valid_body_message()
    if 'expire_date_time' in req_data:
        expire_date_time = req_data['expire_date_time']
    else:
        return valid_body_message()

    if User.query.get(user_id) == None:
        return "User not found", 404

    if Auditorium.query.get(auditorium_id) == None:
        return "Auditorium not found", 404

    if not datetime_validation(auditorium_id, booking_date_time, expire_date_time):
        return "Auditorium on this are already booked", 406

    new_booking = Booking(user_id, auditorium_id, booking_date_time, expire_date_time)
    db.session.add(new_booking)
    db.session.commit()

    return booking_schema.jsonify(new_booking), 201

@app.route('/booking', methods=['GET'])
def get_bookings():
    all_bookings = Booking.query.all()
    result = bookings_schema.dump(all_bookings)
    return jsonify(result)

@app.route('/booking/<booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking == None:
        return "Booking not found",404

    return booking_schema.jsonify(booking)

@app.route('/booking/<booking_id>', methods=['PUT'])
@login_required
def update_booking(booking_id):

    booking = Booking.query.get(booking_id)

    if booking == None:
        return "Booking not found",404


    user_id = request.json['user_id']
    auditorium_id = request.json['auditorium_id']
    booking_date_time = request.json['booking_date_time']
    expire_date_time = request.json['expire_date_time']

    booking.user_id = user_id
    booking.auditorium_id = auditorium_id
    booking.booking_date_time = booking_date_time
    booking.expire_date_time = expire_date_time

    if not datetime_validation(auditorium_id, booking_date_time, expire_date_time):
         return "Auditorium on this are already booked", 406

    db.session.commit()

    return booking_schema.jsonify(booking)

@app.route('/booking/user/<user_id>', methods=['GET'])
@login_required
def get_user_booking(user_id):
    if User.query.get(user_id) == None:
        return "User not found", 404

    all_bookings = Booking.query.all()
    user_bookings = []
    for book in all_bookings:
        if book.user_id == int(user_id):
            user_bookings.append(book)


    result = bookings_schema.dump(user_bookings)
    return jsonify(result)

@app.route('/booking/<booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if booking == None:
        return "Booking not found"

    db.session.delete(booking)
    db.session.commit()
    return booking_schema.jsonify(booking)