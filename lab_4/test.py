import unittest

from flask import json
from flask_bcrypt import Bcrypt

from main import app, db, User, Auditorium, Booking
import base64
header = {
    'Authorization': 'Basic ' + base64.b64encode(b"setup:123").decode("ascii"),
}
wrong_header = {
    'Authorization': 'Basic ' + base64.b64encode(b"wrong:321").decode("ascii"),
}
bcrypt = Bcrypt(app)
class FlaskTestCase (unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()
        db.create_all()
        name = "setup"
        email = "email@em.com"
        password = bcrypt.generate_password_hash("123")
        new_user = User(name, email, password)
        db.session.add(new_user)
        number = 3
        new_auditorium = Auditorium(number)
        db.session.add(new_auditorium)
        db.session.commit()
        user_id = 1
        auditorium_id = 1
        booking_date_time = "2017-04-17T13:30:10"
        expire_date_time = "2017-04-17T18:30:10"
        new_booking = Booking(user_id, auditorium_id, booking_date_time, expire_date_time)
        db.session.add(new_booking)


    def tearDown(self):

        db.session.remove()
        db.drop_all()




    def test_get_users(self):
        response = self.tester.get('/user', content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        #print(header)
        response = self.tester.get('/user/1', headers=header, content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_user_bad(self):
        # print(header)
        response = self.tester.get('/user/1', headers=wrong_header, content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 401)

    def test_register(self):
        response = self.tester.post('user/register', data = json.dumps(dict(
            name = 'test', email = 'test@test.com', password='1234')),
                                    content_type='application/json')

        print(response)
        self.assertEqual(response.status_code, 201)

    def test_register_bad(self):
        response = self.tester.post('user/register', data = json.dumps(dict(
            name = 'test', password='1234')),
                                    content_type='application/json')

        print(response)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = self.tester.get('/login', headers=header, content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_auditoriums(self):
        response = self.tester.get('/auditorium', content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_auditorium(self):
        response = self.tester.get('/auditorium/1', content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_bookings(self):
        response = self.tester.get('/booking', content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_add_auditorium(self):
        response = self.tester.post('/auditorium', headers = header, data=json.dumps(dict(
            number_of_auditorium = 1)), content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 201)

    def test_add_booking(self):
        response = self.tester.post('/booking', data=json.dumps(dict(
           user_id = 1, auditorium_id = 1, booking_date_time = "2018-04-17T13:30:10", expire_date_time = "2018-04-18T13:30:10")),
                                    headers = header, content_type='application/json')

        print(response)
        self.assertEqual(response.status_code, 201)

    def test_get_booking(self):
        # print(header)
        response = self.tester.get('/booking/1', headers=header, content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_booking_by_user(self):
        #print(header)
        response = self.tester.get('/booking/user/1', headers=header, content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_put_booking(self):
        response = self.tester.put('/booking/1', data=json.dumps(dict(
            user_id=1, auditorium_id=1, booking_date_time = "2019-04-17T13:30:10",
            expire_date_time = "2019-04-18T13:30:10")),
                                    headers=header, content_type='application/json')

        print(response)
        self.assertEqual(response.status_code, 200)

    def test_delete_booking(self):
        #print(header)
        response = self.tester.delete('/booking/1', headers=header, content_type = 'application/json')
        print(response)
        self.assertEqual(response.status_code, 200)