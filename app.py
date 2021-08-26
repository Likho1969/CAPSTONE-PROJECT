# Likho Kapesi
# Classroom 2

import hmac
import sqlite3
from flask import Flask, request, redirect
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from flask_mail import Mail, Message
import re
import cloudinary
import cloudinary.uploader
from datetime import timedelta


# creating a user object
class Student(object):
    def __init__(self, email, username, password):
        self.id = email
        self.username = username
        self.password = password


#  service class
class Service(object):
    def __init__(self, service_id, service_name, service_type, service_price, service_image):
        self.service_id = service_id
        self.service_name = service_name
        self.service_type = service_type
        self.service_price = service_price
        self.service_image = service_image


# initializing the database
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('financial_markets.db')
        self.cursor = self.conn.cursor()

    def add_service(self, value):
        query = "INSERT INTO services (service_id, service_name, service_type, service_price," \
                "service_image, email) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, value)

    def delete_service(self, service_id):
        serviceid = service_id
        query = "DELETE FROM services WHERE service_id='" + serviceid + "'"
        self.cursor.execute(query)

    def edit_service(self, service_id, value):
        serviceid = service_id
        values = value
        put_data = {}
        put_data['service_id'] = values.get('service_id')
        put_data['service_name'] = values.get('service_name')
        put_data['service_type'] = values.get('service_type')
        put_data['service_price'] = values.get('service_price')
        put_data['service_image'] = values.get('service_image')

        if values.get('service_image'):
            self.cursor.execute("UPDATE services SET "
                                "service_id=?, "
                                "service_name=?, "
                                "service_type=?, "
                                "service_price=?, "
                                "service_image=? "
                                "WHERE service_id='" + serviceid + "'"
                                ,   (put_data['service_id'],
                                     put_data['service_name'],
                                     put_data['service_type'],
                                     put_data['service_price'],
                                     put_data['service_image']))
        else:
            self.cursor.execute("UPDATE services SET "
                                "service_id=?, "
                                "service_name=?, "
                                "service_type=?, "
                                "service_price=? "
                                "WHERE service_id='" + serviceid + "'"
                                , (put_data['service_id'],
                                   put_data['service_name'],
                                   put_data['service_type'],
                                   put_data['service_price']))

    def select_service(self, value):
        service_id = value
        query = "SELECT * FROM services WHERE service_id='" + service_id + "'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def view_services(self):
        self.cursor.execute("SELECT * FROM services")
        data = self.cursor.fetchall()
        return data

    def edit_student(self, email, value):
        email = email
        values = value
        query = "UPDATE students SET fullName=?, email=?, contact=?, username=?, password=? WHERE email='" + email + "'"
        self.cursor.execute(query, values)

    def select_students(self, value):
        email = value
        query = "SELECT * FROM students WHERE email='" + email + "'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def delete_student(self, email):
        self.cursor.execute("DELETE FROM students WHERE email='" + email + "'")
        self.conn.commit()

    def commit(self):
        return self.conn.commit()


# upload an image and convert it into urls
def upload_file():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name='dlqxdivje', api_key='599819111725767',
                      api_secret='lTD-aqaoTbzVgmZqyZxjPThyaVg')
    upload_result = None
    if request.method == 'POST' or request.method == 'PUT':
        product_image = request.json['product_image']
        app.logger.info('%s file_to_upload', product_image)
        if product_image:
            upload_result = cloudinary.uploader.upload(product_image)
            app.logger.info(upload_result)
            return upload_result['url']


db = Database()


# fetch students from the database
def fetch_students():
    with sqlite3.connect('financial_markets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        users = cursor.fetchall()
        print(users)

        new_data = []

        for data in users:
            new_data.append(Student(data[0], data[4], data[5]))
    return new_data


# fetch services from the database
def fetch_servies():
    with sqlite3.connect('financial_markets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services")
        allproducts = cursor.fetchall()
        print(allproducts)

        new_data = []

        for data in allproducts:
            new_data.append(Service(data[0], data[1], data[2], data[3], data[4]))
    return new_data


students = fetch_students()
services = fetch_servies()


# create the students table in the database
def create_student_table():
    conn = sqlite3.connect('financial_markets.db')
    print("Database opened successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS students(fullName TEXT PRIMARY KEY,"
                 "email TEXT NOT NULL,"
                 "contact TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("students table created successfully")
    conn.close()
    print("Database closed successfully")


# create service table in the database
def create_service_table():
    with sqlite3.connect('financial_markets.db') as conn:
        print("Database opened successfully")
        conn.execute("CREATE TABLE IF NOT EXISTS services (service_id TEXT PRIMARY KEY,"
                     "service_name TEXT NOT NULL,"
                     "service_type TEXT NOT NULL,"
                     "service_price TEXT NOT NULL,"
                     "service_image TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "FOREIGN KEY (email) REFERENCES students (email))")
    print("services table created successfully")
    conn.close()
    print("Database closed successfully")


# create the tables
create_student_table()
create_service_table()


username_table = {u.username: u for u in students}
studentemail_table = {u.id: u for u in students}


# function to create the token during login
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return studentemail_table.get(user_id, None)


# initializing the app
app = Flask(__name__)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)
CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'likhokapesi04@gmail.com'
app.config['MAIL_PASSWORD'] = 'Avuyonke19'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = True
app.config['CORS_HEADERS'] = ['Content-Type']


jwt = JWT(app, authenticate, identity)


@app.route('/protected/')
@jwt_required()
def protected():
    return '%s' % current_identity


#  student registration
@app.route('/student-registration/', methods=["POST"])
def student_registration():
    response = {}
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if request.method == "POST":

        full_name = request.form['fullName']
        email = request.form['email']
        contact = request.form['contact']
        username = request.form['username']
        password = request.form['password']
        if re.search(regex, email):
            with sqlite3.connect("financial_markets.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students("
                               "fullName,"
                               "email,"
                               "contact,"
                               "username,"
                               "password) VALUES(?, ?, ?, ?)", (full_name, email, contact, username, password))
                conn.commit()
                global students
                students = fetch_students()

                response["message"] = "Success. Message has been sent"
                response["status_code"] = 201

            return redirect("/email-sent/%s" % email)
        else:
            return "You have entered an invalid email address. Please enter a valid email address"


#  send an email to users who registered
@app.route('/email-sent/<email>', methods=['GET'])
def send_email(email):
    mail = Mail(app)

    msg = Message('Hello Dear Student', sender='likhokapesi04@gmail.com', recipients=[email])
    msg.body = "You have successfully registered at Dynamic Oak Trading Institute (PTY) LTD."
    mail.send(msg)

    return "Thank you for considering and registering at Dynamic Oak Trading Institute (PTY) LTD."


@app.route("/get-students/<email>/")
@jwt_required()
def get_students(email):
    dtb = Database()
    response = {}
    items = dtb.select_students(email)
    response['status_code'] = 200
    response['data'] = items
    return response


#  view student profile
@app.route('/student-profile/<username>/', methods=["GET"])
def view_student_profile(username):
    response = {}
    if request.method == "GET":
        with sqlite3.connect("financial_markets.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE username='" + username + "'")
            data = cursor.fetchall()
            if data == []:
                return "Student does not exit"
            else:
                response['message'] = 200
                response['data'] = data
        return response


@app.route("/edit-student/<studentemail>/", methods=["PUT"])
@jwt_required()
def edit_student(studentemail):
    response = {}
    dtb = Database()
    if request.method == "PUT":
        full_name = request.json['fullName']
        email = request.json['email']
        contact = request.json['contact']
        username = request.json['username']
        password = request.json['password']
        values = (full_name, email, contact, username, password)
        dtb.edit_student(studentemail, values)
        dtb.commit()
        response['message'] = 200
        return response
    else:
        return "Method not allowed"


@app.route('/delete-student/<email>')
@jwt_required()
def delete_student(email):
    response = {}
    dtb = Database()
    dtb.delete_student(email)
    dtb.commit()
    response['message'] = 200
    response['text'] = "Student Deleted Successfully"
    return response


#  add service to the database
@app.route('/add-service/', methods=["POST"])
@jwt_required()
def add_service():
    dtb = Database()
    response = {}

    if request.method == "POST":
        service_id = request.json['service_id']
        service_name = request.json['service_name']
        service_type = request.json['service_type']
        service_price = request.json['service_price']
        email = request.json['email']
        if (service_id == '' or service_name == '' or service_type == ''
                or service_price == '' or email == ''):
            return "Please fill in all entry fields"
        else:
            if int(service_id):
                values = (service_id, service_name, service_type, service_price, upload_file(), email)
                dtb.add_service(values)
                dtb.commit()

                response["status_code"] = 201
                response['description'] = 'Service added'
                return response
            else:
                return "Please enter service id as a number"
    else:
        return "Method Not Allowed"


@app.route('/select-service/<serviceid>')
@jwt_required()
def select_service(serviceid):
    response = {}
    dtb = Database()
    data = dtb.select_service(serviceid)
    response['message'] = 200
    response['data'] = data
    return response


#  get all service in the database
@app.route('/view-service/', methods=["GET"])
def get_services():
    dtb = Database()
    response = {}
    items = dtb.view_services()
    response['status_code'] = 200
    response['data'] = items
    return response


# delete a service from the database
@app.route("/delete-service/<serviceid>")
@jwt_required()
def delete_service(serviceid):
    response = {}
    dtb = Database()

    dtb.delete_service(serviceid)
    dtb.commit()
    response['status_code'] = 200
    response['message'] = "Service deleted successfully."
    return response


#  edit a service in the database
@app.route("/edit-service/<serviceid>/", methods=["PUT"])
@jwt_required()
def edit_service(serviceid):
    response = {}
    dtb = Database()
    service = dtb.select_service(serviceid)
    if service == []:
        return "Service does not exist in the database"
    else:
        if request.method == "PUT":
            incoming_data = dict(request.json)
            dtb.edit_service(serviceid, incoming_data)
            dtb.commit()
            response['message'] = 200
            return response
        else:
            return "Method not allowed"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
