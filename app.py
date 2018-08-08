from flask import *
import pymongo
app = Flask(__name__)

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
@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		#add to db etc
		myform = request.form
		return render_template('hello.html', name=myform['username'])
	else:
		return render_template('signup.html')