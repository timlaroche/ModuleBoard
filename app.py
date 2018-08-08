from flask import *
from pymongo import *
import bcrypt
app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/newpost")
def newpost():
	return "New post"

@app.route("/admin/<name>")
def admin(name):
	return render_template('admin.html', name=name)

# User Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		loginform = request.form
		db = client.test_db
		collection = db.test_users
		user = collection.find_one({"username": loginform['username']})
		hashed = bcrypt.hashpw(loginform['password'].encode('utf-8'), user['salt'])
		if bcrypt.checkpw(loginform['password'].encode('utf-8'), hashed):
			return render_template('loginsuccess.html', email=user['email'])
		else:
			return "No user with that username/password found."
	else:
		return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		myform = request.form
		#add to db etc
		db = client.test_db
		collection = db.test_users
		userSalt = bcrypt.gensalt()
		password = bcrypt.hashpw(myform['password'].encode('utf-8'), userSalt)
		userinfo = {
			"username": myform['username'],
			"password": password,
			"email": myform['email'],
			"salt": userSalt
		}
		print(collection.insert_one(userinfo).inserted_id)
		return render_template('hello.html', name=myform['username'])
	else:
		return render_template('signup.html')