from flask import *
from pymongo import *
from bson.json_util import *
import bcrypt, json, bson
import datetime
app = Flask(__name__)
#need to regenerate this secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
client = MongoClient('localhost', 27017)

@app.route("/")
def hello():
	url_for('static', filename='style.css')
	return render_template('index.html')

@app.route("/newpost", methods = ['GET', 'POST'])
def newpost():
	if request.method == 'POST':
		#post to db
		#post to test_db, userposts collection, userid tag from session and then contents
		myform = request.form
		db = client.test_db
		collection = db.test_posts
		userPost = {
			"authorID": session['userID'],
			"title": myform['title'],
			"moduleboard": myform['moduleboard'],
			"body": myform['body']
		}
		collection.insert_one(userPost)
		return "post made succesfully"
	else:
		return render_template("newpost.html")

@app.route("/admin/<name>")
def admin(name):
	return render_template('admin.html', name=name)

# EDITOR TESTING #
@app.route("/editortest")
def editortest():
	return render_template("editortest.html")

@app.route("/allposts")
def allposts():
	# find posts in db, return as json
	# read pymongo doc to return slices based on pagination
	# return client.test_db.test_posts.find().fetchall()

	# for now hacky way to display all
	# list comprehensions !! for each post, return a json dump of the posts
	alloftheposts = [post for post in client.test_db.test_posts.find()]
	return dumps(alloftheposts)

@app.route("/viewallposts")
def viewallposts():
	alloftheposts = [post for post in client.test_db.test_posts.find()]
	return render_template("viewallposts.html", posts=alloftheposts)

@app.route("/modules")
def modules():
	return render_template("modules.html")

@app.route("/module/<code>")
def module(code):
	#From the database, get the module name and all other details and pass it into the template
	#render
	db = client.test_db
	collection = db.test_modules
	# Module code, module name
	moduleinfo = collection.find_one({"code" : code})
	# Module board threads
	collection = db.test_posts
	moduleboardthreads = collection.find({"moduleboard" : code})
	return render_template("module.html", moduleinfo=moduleinfo, posts=moduleboardthreads)

@app.route("/module/<code>/<post>")
def modulepost(code, post):
	#Find the post information in the database
	#Handle comments
	db = client.test_db
	collection = db.test_posts
	mypost = collection.find_one({"_id" : ObjectId(post)})
	mycomments = db.test_comments.find({"thread" : str(post)})
	return render_template("post.html", postinfo=mypost, comments=mycomments)

@app.route("/postcomment", methods=['POST'])
def postcomment():
	if session.get('userID'):	
		db = client.test_db
		collection = db.test_comments
		commentform = request.form
		commentdocument = {
			"user_id" : session['userID'],
			"username" : session['username'],
			"comment" : commentform['comment'],
			"thread" : commentform['thread'],
			"date" : datetime.datetime.now(),
			"time" : datetime.datetime.now(),
			"karma" : 1 
		}
		collection.insert_one(commentdocument)
		return "Comment posted"
	else:
		return "Please login to post comments"

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
			session['userID'] = dumps(user['_id'])
			session['username'] = user['username']
			return redirect("/", code=302 )
		else:
			return "No user with that username/password found."
	else:
		return render_template('login.html')

@app.route("/logout", methods=['POST'])
def logout():
	session.clear()
	return redirect('/', code=302)

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
		print(userSalt)
		print(collection.insert_one(userinfo).inserted_id)
		return render_template('hello.html', name=myform['username'])
	else:
		return render_template('signup.html')