# Likho Kapesi
# Classroom 2

import unittest
from app import app


class AppTest(unittest.TestCase):

    # testing whether or not endpoint status codes match (get/push/...) methods
    def test_admin(self):
        test = app.test_client(self)
        response = test.get('/admin')
        status = response.status_code
        self.assertEqual(status, 201)

    def test_edit_admin(self):
        test = app.test_client(self)
        response = test.get('/admin/1')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_add_and_view_client(self):
        test = app.test_client(self)
        response = test.get("/client")
        status = response.status_code
        self.assertEqual(status, 200 or 201)

    def test_edit_client(self):
        test = app.test_client(self)
        response = test.get('/client/NAWCU/')
        status = response.status_code
        self.assertEqual(status, 200, 204)

    def test_view_client(self):
        test = app.test_client(self)
        response = test.get('/view-client/NAWCU')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_service(self):
        test = app.test_client(self)
        response = test.get('/vehicle')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_edit_vehicle(self):
        test = app.test_client(self)
        response = test.get('/vehicle/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_view_service(self):
        test = app.test_client(self)
        response = test.get('/view-vehicle/1')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_add_and_view_service(self):
        test = app.test_client(self)
        response = test.get('/service')
        status = response.status_code
        self.assertEqual(status, 201)

    def test_edit_service(self):
        test = app.test_client(self)
        response = test.get('/service/1')
        status = response.status_code
        self.assertEqual(status, 201)

    def test_appointments(self):
        test = app.test_client(self)
        response = test.get('/appointments')
        status = response.status_code
        self.assertEqual(status, 201)

    def test_edit_appointments(self):
        test = app.test_client(self)
        response = test.get('/appointment/1')
        status = response.status_code
        self.assertEqual(status, 200)

# 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


if __name__ == '__main__':
    unittest.main()
