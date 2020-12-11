from lab_4.data_base import app
from flask import Flask, request, jsonify
from lab_4.data_base import User
from lab_4.data_base import db
from flask_marshmallow import Marshmallow

# ma = Marshmallow(app)
#
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name', 'email', 'password')
#
# user_schema = UserSchema(strict=True)
#
# @app.route('/user/', methods=['POST'])
# def add_user():
#     name = request.json['name']
#     email = request.json['email']
#     password = request.json['password']
#
#     new_user = User(name,email,password)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return user_schema.jsonify(new_user)
#
# @app.route('/bookings/', methods=['GET'])
# def get_all_bookings():
#     return "Here are they all"