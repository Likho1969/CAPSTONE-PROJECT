# Likho Kapesi 
# Classroom 2

import hmac
import sqlite3
import datetime
import cloudinary
import cloudinary.uploader
import validate_email
import DNS
from flask_mail import Mail, Message
from flask import Flask, request, redirect, jsonify
from flask_jwt import JWT, jwt_required
from flask_cors import CORS


####################################################  CREATING TABLES CLASSES START ###################################################

# Creating a user class
class User(object):
    def __init__(self,  id, user_image, name, surname, email, username, password):
        self.id = id
        self.user_image = user_image
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password


# Creating a product class
class Post(object):
    def __init__(self, post_id, post_image, title, intro, body, conclusion, author, date_created, id):
        self.post_id = post_id
        self.post_image = post_image
        self.title = title
        self.intro = intro
        self.body = body
        self.conclusion = conclusion
        self.author = author
        self.date_created = date_created
        self.id = id


# Creating a like class
class Like(object):
    def __init__(self, id, post_id):
        self.id = id
        self.post_id = post_id


# Creating a comment class
class Comment(object):
    def __init__(self, comment_id, comment, id, post_id):
        self.comment_id = comment_id
        self.comment = comment
        self.id = id
        self.post_id = post_id


# Creating a reply class
class Reply(object):
    def __init__(self, reply_id, post_id, user_id, reply, parent_id):
        self.reply_id = reply_id
        self.post_id = post_id
        self.user_id = user_id
        self.text = reply
        self.parent_id = parent_id


# Creating a share class
# class Share(object):
#  def __init__(self, share_id, post_id, user_id, share):
#  self.share_id = share_id
# self.post_id = post_id
# self.user_id = user_id
# self.share = share

# Creating a follow class
# class Follow(object):
# def __init__(self, follow_id, post_id, user_id, follow):
# self.follow_id = follow_id
# self.post_id = post_id
# self.user_id = user_id
# self.follow = follow


####################################################  CREATING TABLES CLASSES ENDS ###################################################


####################################################  DATABASE CLASS START ###################################################


# Creating a database class
class Database(object):
    def __init__(self):
        # Opening blog database
        self.conn = sqlite3.connect('blog.db')
        self.cursor = self.conn.cursor()

    # Registration function
    def registration(self, name, surname, email, username, password):
        self.cursor.execute("INSERT INTO users(user_image ,name, surname, email, username, password) VALUES(? ,?, ?, ?, ?, ?)",
                            (name, surname, email, username, password))
        self.conn.commit()

    # Login function
    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        registered_user = self.cursor.fetchone()
        return registered_user

    # View profile function
    def view_profile(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (str(username)))
        response = self.cursor.fetchone()
        return response

    # Edit user profile function
    def edit_profile(self, incoming_data, username):
        response = {}
        put_data = {}

        # If the user image is edited
        if incoming_data.get('user_image') is not None:
            put_data['user_image'] = incoming_data.get('user_image')

            cloudinary.config(cloud_name='dxgylrfai', api_key='297452228378499',
                              api_secret='lMfu9nSDHtFhnaRTiEch_gfzm_A')
            upload_result = None
            app.logger.info('%s file_to_upload', put_data['user_image'])
            if put_data['user_image']:
                upload_result = cloudinary.uploader.upload(put_data['user_image'])
                app.logger.info(upload_result)
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET user_image =? WHERE username=?", (upload_result['url'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "User image successfully updated"

        # If the name is edited
        if incoming_data.get('name') is not None:
            put_data['name'] = incoming_data.get('name')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name =? WHERE username =?", (put_data['name'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Name successfully updated"

        # If the surname is edited
        if incoming_data.get('surname') is not None:
            put_data['surname'] = incoming_data.get('surname')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET surname =? WHERE username=?", (put_data['surname'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Surname successfully updated"

        # If the email is edited
        if incoming_data.get('email') is not None:
            put_data['email'] = incoming_data.get('email')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET email =? WHERE username=?", (put_data['email'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "ID number successfully updated"

        # If the username is edited
        if incoming_data.get('username') is not None:
            put_data['username'] = incoming_data.get('username')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username =? WHERE username=?", (put_data['username'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Username successfully updated"

        # If the password is edited
        if incoming_data.get('password') is not None:
            put_data['password'] = incoming_data.get('password')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password =? WHERE username=?", (put_data['password'], username))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Password successfully updated"

        return response

    # Delete profile function
    def delete_profile(self, value):
        self.cursor.execute("DELETE FROM users WHERE id='{}'".format(value))
        self.conn.commit()

    # Add new post function
    def create_post(self, post_image, title, intro, body, conclusion, author, id):
        cloudinary.config(cloud_name='dxgylrfai', api_key='297452228378499', api_secret='lMfu9nSDHtFhnaRTiEch_gfzm_A')
        upload_result = None
        app.logger.info('%s file_to_upload', post_image)
        if post_image:
            upload_result = cloudinary.uploader.upload(post_image)
            app.logger.info(upload_result)
        date_created = datetime.datetime.now().strftime("%d/%m/%Y")

        self.cursor.execute("INSERT INTO posts(post_image, title, intro, body, conclusion, author, date_created, id) "
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (upload_result['url'], title, intro, body, conclusion, author, date_created, id))
        self.conn.commit()

    # Edit post function
    def edit_post(self, incoming_data, post_id):
        response = {}
        put_data = {}

        # Edit title of post
        if incoming_data.get('title') is not None:
            put_data['title'] = incoming_data.get('title')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET title =? WHERE post_id=?", (put_data['title'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Title was successfully updated."

        # Edit image of post
        if incoming_data.get('post_image') is not None:
            put_data['post_image'] = incoming_data.get('post_image')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET post_image =? WHERE post_id=?", (put_data['post_image'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Image was successfully updated."

        # Edit intro of post
        if incoming_data.get('intro') is not None:
            put_data['intro'] = incoming_data.get('intro')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET intro =? WHERE post_id=?", (put_data['intro'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Introduction was successfully updated."

        # Edit body of post
        if incoming_data.get('body') is not None:
            put_data['body'] = incoming_data.get('intro')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET body =? WHERE post_id=?", (put_data['body'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Body was successfully updated."

        # Edit conclusion of post
        if incoming_data.get('conclusion') is not None:
            put_data['conclusion'] = incoming_data.get('intro')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET conclusion =? WHERE post_id=?", (put_data['conclusion'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Conclusion was successfully updated."

        # Edit author of post
        if incoming_data.get('author') is not None:
            put_data['author'] = incoming_data.get('author')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET author =? WHERE post_id=?", (put_data['author'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Author was successfully updated."

        # Edit date created of post
        if incoming_data.get('date_created') is not None:
            put_data['date_created'] = incoming_data.get('date_created')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET date_created =? WHERE post_id=?", (put_data['date_created'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Creation date was successfully updated."

        # Edit user id of post
        if incoming_data.get('id') is not None:
            put_data['id'] = incoming_data.get('author')
            with sqlite3.connect('blog.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE posts SET id =? WHERE post_id=?", (put_data['id'], post_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "User id was successfully updated."

        return response

    # Deleting post function
    def delete_post(self, value):
        self.cursor.execute("DELETE FROM posts WHERE post_id='{}'".format(value))
        self.conn.commit()

    # Displaying all posts function
    def show_posts(self):
        self.cursor.execute("SELECT * FROM posts")
        return self.cursor.fetchall()

    # Display a post function
    def view_post(self, value):
        self.cursor.execute("SELECT * FROM posts WHERE post_id='{}'".format(value))
        response = self.cursor.fetchone()
        return response

    # Display a specific users posts function
    def view_users_posts(self, value):
        self.cursor.execute("SELECT * FROM posts WHERE id='{}'".format(value))
        return self.cursor.fetchall()

    # Creating a like function
    def like(self, username, post_id):
        self.cursor.execute("INSERT INTO likes(username, post_id) VALUES(?, ?)", (username, post_id))
        self.conn.commit()

    # Displays likes on a post function
    def display_likes(self, post_id):
        self.cursor.execute("SELECT * FROM likes WHERE post_id='{}'".format(post_id))
        return self.cursor.fetchall()

    # Adding a comment function
    def add_comment(self, comment, username, post_id):
        self.cursor.execute("INSERT INTO comments(comment, username, post_id) VALUES(?, ?, ?)",
                            (comment, username, post_id))
        self.conn.commit()

    # Display comment function
    def display_comments(self, value):
        self.cursor.execute("SELECT * FROM comments WHERE post_id='{}'".format(value))
        return self.cursor.fetchall()

    # Editing a comment function
    def edit_comment(self, comment, comment_id):
        self.cursor.execute("UPDATE comments SET comment='{}' WHERE comment_id='{}'".format(comment, comment_id))
        self.conn.commit()

    # Deleting a comment function
    def delete_comment(self, value):
        self.cursor.execute("DELETE FROM comments WHERE comment_id='{}'".format(value))
        self.conn.commit()

    # Adding a reply function
    def add_reply(self, reply, username, post_id):
        self.cursor.execute("INSERT INTO replies(reply, username, post_id) VALUES(?, ?, ?)",
                            (reply, username, post_id))
        self.conn.commit()

    # Display reply function
    def display_reply(self, value):
        self.cursor.execute("SELECT * FROM replies WHERE reply_id='{}'".format(value))
        return self.cursor.fetchall()

    # Editing a reply function
    def edit_reply(self, reply, reply_id):
        self.cursor.execute("UPDATE replies SET replies='{}' WHERE reply_id='{}'".format(reply, reply_id))
        self.conn.commit()

    # Deleting a reply function
    def delete_reply(self, value):
        self.cursor.execute("DELETE FROM replies WHERE reply_id='{}'".format(value))
        self.conn.commit()

    # Follow user function   
    # def follow_user(self, userid1, userid2):
    #  self.cursor.execute("SELECT * FROM users WHERE userId='" + str(userid2) + "'")
    # data = self.cursor.fetchone()
    # followingstring = data['following']
    # followerstring = data['followers']

    # if followingstring is not None:
    # if len(list(data['following'])) != 1:
    #  newfollowarray = list(map(int, followingstring[1:len(followingstring)-1].split(",")))

    # elif len(list(data['following'])) < 2:
    # newfollowarray = [int(followingstring)]

    # newfollowarray.append(userid1)
    # newfollowingstring = str(newfollowarray)
    # self.cursor.execute("UPDATE users SET following=? WHERE userId=?", (newfollowingstring, userid2))
    # self.conn.commit()

    # else:
    # self.cursor.execute("UPDATE users SET following=? WHERE userId=?", (userid1, userid2))
    # self.conn.commit()

    # self.cursor.execute("SELECT * FROM users WHERE userId='" + str(userid1) + "'")
    # data = self.cursor.fetchone()

    # if data['followers'] is not None:
    # if len(list(data['followers'])) > 1:
    # newfollowerarray = list(map(int, followerstring[1:len(data['followers']) - 1].split(",")))

    # if len(list(data['followers'])) < 2:
    #  newfollowerarray = [followerstring]

    # newfollowerarray.append(userid2)
    # newfollowerstring = str(newfollowerarray)
    # self.cursor.execute("UPDATE users SET followers=? WHERE user_id=?", (newfollowerstring, userid1))
    # self.conn.commit()
    # else:
    # self.cursor.execute("UPDATE users SET followers=? WHERE user_id=?", (userid2, userid1))
    # self.conn.commit()

    # def time_now():
    #  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Retweet function       
    # def share_post(self, userid, post_id):
    #  self.cursor.execute("SELECT * FROM posts WHERE post_id='" + str(post_id) + "'")
    # data = self.cursor.fetchone()
    # user_id = data['userId']
    # source_id = postid
    # retweetedby = userid
    # time = data['datetime']
    # if data['text'] is not None:
    # if data['image1'] is None:
    # self.cursor.execute("INSERT INTO posts("
    #  "userId,"
    # "sourceId,"
    # "retweeted_by,"
    # "text,"
    # "created_time,"
    # "datetime) VALUES(?, ?, ?, ?, ?, ?)", (user_id,
    #  source_id,
    # retweetedby,
    # data['text'],
    # time_now(),
    # time))


####################################################  DATABASE CLASS END ###################################################


####################################################  CREATING TABLES START ###################################################

# Creating a user table
def init_user_table():
    conn = sqlite3.connect('blog.db')
    print("Opened database successfully.")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "user_image TEXT,"
                 "name TEXT NOT NULL,"
                 "surname TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("pser table created successfully.")
    conn.close()


# Create a blog post table
def init_post_table():
    with sqlite3.connect('blog.db') as conn:
        print("Opened database successfully.")
        conn.execute("CREATE TABLE IF NOT EXISTS posts(post_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "post_image TEXT NOT NULL,"
                     "title TEXT NOT NULL,"
                     "intro TEXT NOT NULL,"
                     "body TEXT NOT NULL,"
                     "conclusion TEXT NOT NULL,"
                     "author TEXT NOT NULL,"
                     "date_created TEXT NOT NULL,"
                     "id INTEGER NOT NULL,"
                     "FOREIGN KEY (id) REFERENCES users(id))")
    print("post table created successfully.")


# Create a like table
def init_like_table():
    with sqlite3.connect('blog.db') as conn:
        print("Opened database successfully.")
        conn.execute("CREATE TABLE IF NOT EXISTS likes(username TEXT NOT NULL, post_id TEXT NOT NULL,"
                     "FOREIGN KEY (username) REFERENCES users(username),"
                     "FOREIGN KEY (post_id) REFERENCES posts(post_id))")
    print("like table created successfully.")


# Create a comment table
def init_comment_table():
    with sqlite3.connect('blog.db') as conn:
        print("Opened database successfully.")
        conn.execute("CREATE TABLE IF NOT EXISTS comments(comment_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "comment TEXT NOT NULL,"
                     "username TEXT NOT NULL,"
                     "post_id TEXT NOT NULL,"
                     "FOREIGN KEY (username) REFERENCES users(username),"
                     "FOREIGN KEY (post_id) REFERENCES posts(post_id))")
    print("comment table created successfully.")


def init_reply_table():
    conn = sqlite3.connect('blog.db')
    print("Opened database successfully.")
    conn.execute("CREATE TABLE IF NOT EXISTS replies(reply_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "post_id INTEGER NOT NULL,"
                 "user_id INTEGER NOT NULL,"
                 "reply TEXT NOT NULL,"
                 "parentId INTEGER,"
                 "FOREIGN KEY (post_id) REFERENCES posts (post_id),"
                 "FOREIGN KEY (user_id) REFERENCES users (user_id))")
    print("user table created successfully.")
    conn.close()


# def init_share_table():
#  conn = sqlite3.connect('blog.db')
#  print("Opened database successfully.")
#  conn.execute("CREATE TABLE IF NOT EXISTS share(share_id INTEGER PRIMARY KEY AUTOINCREMENT,"
#              "post_id INTEGER NOT NULL,"
#              "user_id INTEGER NOT NULL,"
#              "share TEXT NOT NULL,"
#              "FOREIGN KEY (username) REFERENCES users(username),"
#              "FOREIGN KEY (id) REFERENCES posts(id))")
# print("share table created successfully.")

# def init_follow_table():
#  conn = sqlite3.connect('blog.db')
#  print("Opened database successfully.")
#  conn.execute("CREATE TABLE IF NOT EXISTS follow(follow_id INTEGER PRIMARY KEY AUTOINCREMENT,"
#               "post_id INTEGER NOT NULL,"
#               "user_id INTEGER NOT NULL,"
#               "follow TEXT NOT NULL,"
#               "FOREIGN KEY (username) REFERENCES users(username),"
#               "FOREIGN KEY (id) REFERENCES posts(id))")
#  print("follow table created suuccessfully.")

####################################################  CREATING TABLES ENDS ###################################################


####################################################  FETCHING FROM DATABASE START ###################################################

# Fetching all users
def fetch_users():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

    return new_data


# Fetching all blogs
def fetch_blog_posts():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()

        new_data = []

        for data in posts:
            new_data.append(Post(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    return new_data


# Fetching all likes
def fetch_likes():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM likes")
        likes = cursor.fetchall()

        new_data = []

        for data in likes:
            new_data.append(Like(data[0], data[1]))
    return new_data


# Fetching all comments
def fetch_comments():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments")
        comments = cursor.fetchall()

        new_data = []

        for data in comments:
            new_data.append(Comment(data[0], data[1], data[2], data[3]))
    return new_data


# Fetching all replies
def fetch_replies():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM replies")
        replies = cursor.fetchall()

        new_data = []

        for data in replies:
            new_data.append(Reply(data[0], data[1], data[2], data[3], data[4]))
    return new_data


# Fetch all shared 
# def fetch_shared():
#  with sqlite3.connect('blog.db') as conn:
#   cursor = conn.cursor()
#   cursor.execute("SELECT * FROM share")
#   share = cursor.fetchall()

#   new_data = []

#   for data in share:
#      new_data.append(Share(data[0], data[1], data[2], data[3]))


# Fetching all followers
# def fetch_followers():
# with sqlite3.connect('blog.db') as conn:
#   cursor = conn.cursor()
#   cursor.execute("SELECT * FROM followers")
#   followers = cursor.fetchall()

#   new_data = []

#   for data in followers:
#      new_data.append(Follow(data[0], data[1], data[2], data[3]))


####################################################  FETCHING FROM DATABASE END ###################################################


####################################################  TABLE INITIALIZIATION START ###################################################


# Initializing user table
init_user_table()
# Initializing product table
init_post_table()
# Initializing like table
init_like_table()
# Initializing comment table
init_comment_table()
# Initializing reply table
init_reply_table()
# Initializing share table
# init_share_table()
# Initializng followers table
# init_follow_table()


####################################################  TABLE INITIALIZIATION END ###################################################


####################################################  CALLING FETCHING FUNCTIONS START ###################################################

# Creating list of all users
users = fetch_users()
# Creating a list of all the posts
blog_posts = fetch_blog_posts()
# Creating list of all likes
likes = fetch_likes()
# Creating list of all comments
comments = fetch_comments()
# Creating list of all replies
replies = fetch_replies()
# Creating list of shared 
# shared = fetch_shared()
# Creating list of followers
# followers = fetch_followers()


####################################################  CALLING FETCHING ENDS ###################################################


####################################################  APP START ###################################################

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    users = fetch_users()
    username_table = {u.username: u for u in users}
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    users = fetch_users()
    userid_table = {u.id: u for u in users}
    user_id = payload['identity']
    return userid_table.get(user_id, None)


# App initialized
app = Flask(__name__)

CORS(app, resource={r"/*": {"origins": "*"}})
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# Extends the jwt tokens validation time to 20 hours
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=24)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# Senders email
app.config['MAIL_USERNAME'] = 'likhokapesi135@gmail.com'
# Senders password
app.config['MAIL_PASSWORD'] = 'Politician1969'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

jwt = JWT(app, authenticate, identity)


# User registration route
@app.route('/registration/', methods=["POST"])
def registration():
    db = Database()
    response = {}

    if request.method == "POST":

        user_image = request.form['user_image']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username='{}'".format(username))
            registered_username = cursor.fetchone()

        # Creates an error if all fields aren't filled out
        if user_image == '' or name == '' or surname == '' or email == '' or username == '' or password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter all fields."
            return response

        # Checks if the email is valid
        elif not validate_email.validate_email(email, verify=True):
            response['status_code'] = 400
            response['message'] = "Error! Please enter a valid email address."
            return response

        # Checks if the username exists already
        elif registered_username:
            response['status_code'] = 400
            response['message'] = "Username already taken. Please enter a unique username."
            return response

        else:
            db.registration(name, surname, email, username, password)
            response["message"] = "New user registered successfully"
            response["status_code"] = 200

            global users
            users = fetch_users()

        return redirect("/send-email/%s" % email)


# App route to send an email once a user has successfully registered
@app.route('/send-email/<email>', methods=["GET"])
def send_email(email):
    response = {}
    mail = Mail(app)
    msg = Message("Welcome!", sender='likhokapesi135@gmail.com', recipients=[email])
    msg.body = "Good morning/afternoon/Evening.\n You have successfully registered your profile on our site.\n" \
               "Please feel free to send us an email if you have any queries or concerns.\n \n" \
               "Kind Regards,\n SocialBook Team."
    mail.send(msg)

    response["message"] = "User successfully registered, Please check your email."
    response["status_code"] = 200

    return response


# App route to login
@app.route('/login/', methods=["POST"])
def login():
    response = {}

    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            registered_user = cursor.fetchone()

        # If username is empty it creates an error
        if username == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your username."
            return response

        # If password is empty it creates an error
        if password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your password."
            return response

        # Checks if the user exists in the database
        if registered_user:
            response['registered_user'] = registered_user
            response['status_code'] = 200
            response['message'] = "Successfully logged in"
            return response

        else:
            response['status_code'] = 400
            response['message'] = "Login unsuccessful. Please try again."
        return jsonify(response)


# App route for the user to view their profile
@app.route('/view-profile/<username>/', methods=["GET"])
@jwt_required()
def view_profile(username):
    response = {}

    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username='{}'".format(username))

        response['status_code'] = 200
        response['message'] = "Profile retrieved successfully"
        response['data'] = cursor.fetchone()

    return jsonify(response)


# App route for the user to edit their profile
@app.route('/edit-profile/<username>/', methods=["PUT"])
@jwt_required()
def edit_profile(username):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        response = db.edit_profile(incoming_data, username)

    return response


# App route for the user to delete their profile
@app.route('/delete-profile/<username>/')
@jwt_required()
def delete_profile(username):
    response = {}
    db = Database()
    db.delete_profile(username)

    response['status_code'] = 200
    response['message'] = "Profile deleted successfully"
    return response


# App route to display all users route
@app.route('/display-all-users/', methods=["GET"])
def display_users():
    response = {}
    with sqlite3.connect("blog.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")

        all_users = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = all_users
    return response


# App route to display a specific user route
@app.route('/display-one-user/<username>/', methods=["GET"])
def display_one_user(username):
    response = {}
    with sqlite3.connect("blog.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username='" + username + "'")

        one_user = cursor.fetchone()

    response['status_code'] = 200
    response['data'] = one_user
    return response


# App route for the user to create a post
@app.route('/create-post/', methods=["POST"])
@jwt_required()
def create_post():
    db = Database()
    response = {}

    if request.method == "POST":
        image = request.files['post_image']
        title = request.form['title']
        intro = request.form['intro']
        body = request.form['body']
        conclusion = request.form['conclusion']
        author = request.form['author']
        id = request.form['id']

        db.create_post(image, title, intro, body, conclusion, author, id)
        response["status_code"] = 200
        response['description'] = "Post created successfully"
        return response


# App route for the user to delete a blog post
@app.route('/delete-post/<int:post_id>/')
@jwt_required()
def delete_post(post_id):
    db = Database()
    response = {}
    db.delete_post(post_id)
    response['status_code'] = 200
    response['message'] = "Post deleted successfully"
    return response


# App route for the user to edit their post
@app.route('/edit-post/<int:post_id>/', methods=["PUT"])
@jwt_required()
def edit_post(post_id):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        response = db.edit_post(incoming_data, post_id)

    return response


# App route to display all the posts from the database
@app.route('/show-posts/', methods=["GET"])
def show_posts():
    db = Database()
    response = {}

    posts = db.show_posts()
    response['status_code'] = 200
    response['data'] = posts
    return response


# App route to view a specific post
@app.route('/view-post/<int:post_id>/', methods=["GET"])
def view_post(post_id):
    db = Database()
    response = {}

    data = db.view_post(post_id)
    response['data'] = data
    response['status_code'] = 200
    response['description'] = "Post retrieved successfully"

    return jsonify(response)


# App route to view a specific user's posts
@app.route('/view-users-posts/<int:id>/', methods=["GET"])
def view_users_products(id):
    response = {}
    db = Database()

    user_posts = db.view_users_posts(id)
    response['status_code'] = 200
    response['message'] = "All posts retrieved successfully"
    response['data'] = user_posts

    return response


# App route to like a post
@app.route('/like-post/', methods=["POST"])
@jwt_required()
def like_post():
    response = {}
    db = Database()

    if request.method == "POST":
        username = request.json['username']
        post_id = request.json['post_id']

        db.like(username, post_id)
        response['status_code'] = 200
        response['message'] = "Post liked successfully"
        return response


# App route to display all likes on a post
@app.route('/display-likes/<int:post_id>/', methods=["GET"])
def display_likes(post_id):
    response = {}
    db = Database()

    likes = db.display_likes(post_id)
    response['data'] = likes
    response['status_code'] = 200
    response['message'] = "All likes retrieved successfully"
    return response


# App route to add a comment to a post
@app.route('/add-comment/', methods=["POST"])
@jwt_required()
def add_comment():
    response = {}
    db = Database()

    if request.method == "POST":
        comment = request.json['comment']
        username = request.json['username']
        post_id = request.json['post_id']

        db.add_comment(comment, username, post_id)
        response['status_code'] = 200
        response['message'] = "Comment added successfully"
        return response


# App route to display comments
@app.route('/display-comments/<post_id>/', methods=["GET"])
def display_comments(post_id):
    response = {}
    db = Database()

    comments = db.display_comments(post_id)
    response['status_code'] = 200
    response['message'] = "All comments retrieved successfully"
    response['data'] = comments
    return response


# App route to edit a comment
@app.route('/edit-comment/<int:comment_id>/', methods=["PUT"])
@jwt_required()
def edit_comment(comment_id):
    response = {}
    db = Database()

    if request.method == "PUT":
        comment = request.json['comment']
        db.edit_comment(comment, comment_id)
        response['status_code'] = 200
        response['message'] = "Comment edited successfully"
    return response


# App route to delete a comment
@app.route('/delete-comment/<int:comment_id>/')
@jwt_required()
def delete_comment(comment_id):
    response = {}
    db = Database()

    db.delete_comment(comment_id)
    response['status_code'] = 200
    response['message'] = "Comment deleted successfully"
    return response


# App route to add a reply to a post
@app.route('/add-reply/', methods=["POST"])
@jwt_required()
def add_reply():
    response = {}
    db = Database()

    if request.method == "POST":
        reply = request.json['reply']
        username = request.json['username']
        post_id = request.json['post_id']

        db.add_reply(reply, username, post_id)
        response['status_code'] = 200
        response['message'] = "Reply added successfully"
        return response


# App route to display replies
@app.route('/display-reply/<reply_id>/', methods=["GET"])
def display_reply(post_id):
    response = {}
    db = Database()

    replies = db.display_reply(post_id)
    response['status_code'] = 200
    response['message'] = "All replies retrieved successfully"
    response['data'] = replies
    return response


# App route to edit a reply
@app.route('/edit-reply/<int:reply_id>/', methods=["PUT"])
@jwt_required()
def edit_reply(reply_id):
    response = {}
    db = Database()

    if request.method == "PUT":
        reply = request.json['reply']
        db.edit_reply(reply, reply_id)
        response['status_code'] = 200
        response['message'] = "Reply edited successfully"

    return response


# App route to delete a reply
@app.route('/delete-reply/<int:reply_id>/')
@jwt_required()
def delete_reply(reply_id):
    response = {}
    db = Database()

    db.delete_reply(reply_id)
    response['status_code'] = 200
    response['message'] = "Reply deleted successfully"
    return response


# App route for user to share a post
# @app.route('/post/share/<username>/<int:post_id>', methods=["POST"])
# def share(username, post_id):
#  response = {}
# db = Database()
# if request.method == "POST":
#    db.share_post(username, post_id)
#   db.commit()

#  response['message'] = "Post shared successfully"
# response['status_code'] = 200

# return response


# App route for following a user
# @app.route('/user/follow/<int:userid1>/<int:userid2>/', methods=['PATCH'])
# def follow_user(userid1, userid2):
#  response = {}
# db = Database()

# if request.method == 'PATCH':
#     db.follow_user(userid1, userid2)
#     response['message'] = 'User followed successfully'
#     response['status_code'] = 200
#     return response


# App route for unfollowing a user
# @app.route('/user/delete-follow/<int:userid1>/<int:userid2>/')
# def unfollow_user(userid1, userid2):
#  response = {}
#  db = Database()

#  db.unfollow_user(userid1, userid2)
#  response['status_code'] = 200
#  response['message'] = "User unfollowed successfully"
#  return response


####################################################  APP ENDS ###################################################


if __name__ == '__main__':
    app.run()
