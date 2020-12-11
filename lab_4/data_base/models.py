# from lab_4.data_base import  db
# from datetime import datetime
#
# class User(db.Model):
#
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(70), unique=True, nullable=False)
#     email = db.column(db.String(70), unique=True,  nullable=False)
#     password = db.Column(db.String(70),nullable=False)
#
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password
#
#
# class Auditorium(db.Model):
#     __tablename__ = "auditoriums"
#     id = db.Column(db.Integer, primary_key=True)
#     number_of_auditorium = db.Column(db.Integer, unique=True, nullable=False)
#
#     def __init__(self, number):
#         self.number_of_auditorium = number
#
# class Booking(db.Model):
#     __tablename__ = "bookings"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"), nullable=False)
#     auditorium_id = db.Column(db.Integer, db.ForeignKey('auditorium.id', ondelete="cascade"), nullable=False)
#     booking_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     expire_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#
#     def __init__(self, user_id, auditorium_id, booking_date_time, expire_date_time):
#         self.user_id = user_id
#         self.auditorium_id = auditorium_id
#         self.booking_date_time = booking_date_time
#         self.expire_date_time = expire_date_time
#
#
#
#
#
