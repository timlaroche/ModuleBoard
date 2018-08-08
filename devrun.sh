mongod --fork --dbpath data/db
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run