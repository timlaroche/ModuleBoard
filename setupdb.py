import re
from pymongo import *

client = MongoClient('localhost', 27017)
db = client.test_db
modulefile = open("modulelist", "r")

for line in modulefile:
	moduleinfo = line.split('-')
	db.test_modules.insert_one({
		"code" : moduleinfo[0].strip(),
		"name" : moduleinfo[1].strip()
		})