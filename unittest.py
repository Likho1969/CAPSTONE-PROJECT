# Likho Kapesi
# Classroom 2

import unittest
from app import app


class Testing_App(unittest.app):

    # testing whether or not endpoint status codes match (get/push/...) methods
    def test_student_registration(self):
        test = app.test_client(self)
        response = test.get('/student-registration/')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_email(self):
        test = app.test_client(self)
        response = test.get('/email-sent/kapesilikho166@gmail.com@gmail.com')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_message(self):
        test = app.test_client(self)
        response = test.get("/message-sent/0637844770")
        status = response.status_code
        self.assertEqual(status, 201)

    def test_view_student_profile(self):
        test = app.test_client(self)
        response = test.get('/student-profile/NAWCU/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_add_service(self):
        test = app.test_client(self)
        response = test.get('/add-/')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_view_service(self):
        test = app.test_client(self)
        response = test.get('/view-service/')
        status = response.status_code
        self.assertEqual(status, 200)

    # checking content type
    # def test_type_view_service(self):
     # test = app.test_client(self)
       # response = test.get('/view-service/')
        # self.assertEqual(response.content_type, "application/json")
