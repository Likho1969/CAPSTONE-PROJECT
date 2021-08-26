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


# creating a product object
class Product(object):
    def __init__(self, product_id, product_name, product_type, product_quantity, product_price, product_image):
        self.product_id = product_id
        self.product_name = product_name
        self.product_type = product_type
        self.product_quantity = product_quantity
        self.product_price = product_price
        self.product_image = product_image


# initializing the database
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('financial_markets.db')
        self.cursor = self.conn.cursor()

    def addpro(self, value):
        query = "INSERT INTO services (service_id, service_name, service_type, service_price," \
                "service_image, email) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, value)

    def delpro(self, productid):
        proid = productid
        query = "DELETE FROM catalogue WHERE service_id='" + proid + "'"
        self.cursor.execute(query)

    def editpro(self, pro_id, value):
        proid = pro_id
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
                                "WHERE service_id='" + proid + "'"
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
                                "WHERE service_id='" + proid + "'"
                                , (put_data['service_id'],
                                   put_data['service_name'],
                                   put_data['service_type'],
                                   put_data['service_price']))

    def edituser(self, email, value):
        email = email
        values = value
        query = "UPDATE students SET fullName=?, email=?, contact=?, password=? WHERE email='" + email + "'"
        self.cursor.execute(query, values)

    def selectproduct(self, value):
        proid = value
        query = "SELECT * FROM students WHERE service_id='" + proid + "'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def myproducts(self, value):
        email = value
        query = "SELECT * FROM students WHERE email='" + email + "'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def viewcat(self):
        self.cursor.execute("SELECT * FROM students")
        data = self.cursor.fetchall()
        return data

    def deleteuser(self, email):
        self.cursor.execute("DELETE FROM students WHERE email='" + email + "'")
        self.conn.commit()

    def commit(self):
        return self.conn.commit()


# function to take image uploads and convert them into urls
def upload_file():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name='dlqxdivje', api_key='599819111725767',
                      api_secret='lTD-aqaoTbzVgmZqyZxjPThyaVg')
    upload_result = None
    if request.method == 'POST' or request.method == 'PUT':
        product_image = request.json['service_image']
        app.logger.info('%s file_to_upload', product_image)
        if product_image:
            upload_result = cloudinary.uploader.upload(product_image)
            app.logger.info(upload_result)
            return upload_result['url']


db = Database()


# collecting all users from the database
def fetch_students():
    with sqlite3.connect('financial_markets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        print(students)

        new_data = []

        for data in students:
            new_data.append(Student(data[0], data[4], data[5]))
    return new_data


# collecting all products from the database
def fetch_services():
    with sqlite3.connect('financial_markets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services")
        services = cursor.fetchall()
        print(services)

        new_data = []

        for data in services:
            new_data.append(Product(data[0], data[1], data[2], data[3], data[4], data[5]))
    return new_data


students = fetch_students()
products = fetch_services()


# function to create the user table in the database
def createstudenttable():
    conn = sqlite3.connect('financial_markets.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS students(student_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "fullName TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "contact TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("user table created successfully")
    conn.close()


#  create the products table in the database
def createservicetable():
    with sqlite3.connect('financial_markets.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS services (service_id TEXT NOT NULL,"
                     "service_name TEXT NOT NULL,"
                     "service_type TEXT NOT NULL,"
                     "service_price TEXT NOT NULL,"
                     "service_image TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "FOREIGN KEY (email) REFERENCES students (email))")
    print("product table created successfully.")


# call functions to create the tables
createstudenttable()
createservicetable()


username_table = {u.username: u for u in students}
useremail_table = {u.id: u for u in students}


# function to create the token during login
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return useremail_table.get(user_id, None)


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


# student registration
@app.route('/student-registration/', methods=["POST"])
def user_registration():
    response = {}
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if request.method == "POST":

        fullName = request.form['fullName']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        if (re.search(regex, email)):
            with sqlite3.connect("financial_markets.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students("
                               "fullName,"
                               "email,"
                               "contact,"
                               "password) VALUES(?, ?, ?, ?, ?, ?)", (fullName, email, contact, password))
                conn.commit()
                global users
                users = fetch_students()

                response["message"] = "Success. Message has been sent"
                response["status_code"] = 201

            return redirect("/email-sent/%s" % email)
        else:
            return "Email not valid. Please enter a valid email address"


#  send an email to student who registered
@app.route('/email-sent/<email>', methods=['GET'])
def sendemail(email):
    mail = Mail(app)

    msg = Message('Hello Student', sender='likhokapesi04@gmail.com', recipients=[email])
    msg.body = "You have successfully registered registered at Dynamic Oak Trading Institute (PTY) LTD."
    mail.send(msg)

    return "Thank you for registering at and considering Dynamic Oak Trading Institute (PTY) LTD."


# app route to view a profile
@app.route('/show-student/<username>/', methods=["GET"])
def viewownprofile(username):
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


# app route to add a product to the database
@app.route('/add-service/', methods=["POST"])
@jwt_required()
def newproduct():
    dtb = Database()
    response = {}

    if request.method == "POST":
        service_id = request.json['service_id']
        service_name = request.json['service_name']
        service_type = request.json['service_type']
        service_price = request.json['service_price']
        email = request.json['email']
        if (service_id == '' or service_name == '' or service_type == '' or service_price == '' or email == ''):
            return "You are advised to fill in all the required entry fields"
        else:
            if int(service_id):
                values = (service_id, service_name, service_type, service_price, upload_file(), email)
                dtb.addpro(values)
                dtb.commit()

                response["status_code"] = 201
                response['description'] = 'Service Added Successfully'
                return response
            else:
                return "You are advised to enter service id as an number"
    else:
        return "Method Not Allowed"


# app route to view all the products in the database
@app.route('/show-service/', methods=["GET"])
def get_products():
    dtb = Database()
    response = {}
    items = dtb.viewcat()
    response['status_code'] = 200
    response['data'] = items
    return response


# app route to delete a product from the database
@app.route("/delete-service/<serviceid>")
@jwt_required()
def delete_product(serviceid):
    response = {}
    dtb = Database()

    dtb.delpro(serviceid)
    dtb.commit()
    response['status_code'] = 200
    response['message'] = "Service deleted successfully."
    return response


# app route to edit a product in the database
@app.route("/edit-service/<serviceid>/", methods=["PUT"])
@jwt_required()
def edit_product(serviceid):
    response = {}
    dtb = Database()
    product = dtb.selectproduct(serviceid)
    if product == []:
        return "Service does not exist in the database"
    else:
        if request.method == "PUT":
            incoming_data = dict(request.json)
            dtb.editpro(serviceid, incoming_data)
            dtb.commit()
            response['message'] = 200
            return response
        else:
            return "Method not allowed"


@app.route("/our-service/<email>/")
@jwt_required()
def getmyproducts(email):
    dtb = Database()
    response = {}
    items = dtb.myproducts(email)
    response['status_code'] = 200
    response['data'] = items
    return response


@app.route("/edit-student/<studentemail>/", methods=["PUT"])
@jwt_required()
def edit_user(useremail):
    response = {}
    dtb = Database()
    if request.method == "PUT":
        fullName= request.json['fullName']
        email = request.json['email']
        contact = request.json['contact']
        password = request.json['password']
        values = (fullName, email, contact, password)
        dtb.edituser(useremail, values)
        dtb.commit()
        response['message'] = 200
        return response
    else:
        return "Method not allowed"


@app.route('/select-service/<serviceid>')
@jwt_required()
def selectitem(productid):
    response = {}
    dtb = Database()
    data = dtb.selectproduct(productid)
    response['message'] = 200
    response['data'] = data
    return response


@app.route('/delete-student/<email>')
@jwt_required()
def deleteuser(email):
    response = {}
    dtb = Database()
    dtb.delpro(email)
    dtb.commit()
    dtb.deleteuser(email)
    response['message'] = 200
    response['text'] = "Student successfully deleted"
    return response


if __name__ == '__main__':
    app.run(debug=True)
