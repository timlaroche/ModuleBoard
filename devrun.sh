mongod --fork --dbpath data/db --logpath log/mongod.log
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
