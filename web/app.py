"""
Registration of a user
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)


client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
	def post(self):
		#Step 1: Get posted data by the user:
		postedData = request.get_json()

		#Get the data:
		username = postedData["username"]
		password = postedData["password"]

		hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

		#Store username and pw into the database:
		users.insert({
			"Username": username,
			"Password": hashed_pw,
			"Sentence": "",
			"Tokens":6
			})

		retJson = {
			"status": 200,
			"msg": "You successfully signed up for the API"
		}
		return jsonify(retJson)

def verifyPw(username, password):
	hashed_pw = users.find({
			"Username":username
		})[0]["Password"]

	if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
		return True
	else:
		return False

def countTokens(username):
	tokens = users.find({
			"Username":username
	})[0]["Tokens"]
	return tokens


class Store(Resource):
	def post(self):
		#Step 1: Get posted data by the user:
		postedData = request.get_json()

		#Step 2: Read the data:	
		username = postedData["username"]
		password = postedData["password"]
		sentence = postedData["sentence"]

		#Step 3: Verify the username and pw match:
		correct_pw = verifyPw(username, password)

		if not correct_pw:
			retJson = {
				"status":302
			}
			return jsonify(retJson)

		#Step 4: Verify if user has enough tokens:
		num_tokens = countTokens(username)

		if num_tokens <= 0:
			retJson = {
				"status":301
			}
			return jsonify(retJson)

		#Step 5: Store the sentence, take one token away and return 200-OK:
		users.update({
				"Username":username
		}, {
			"$set":{
				"Sentence":sentence,
				"Tokens":num_tokens-1
				}
		})

		retJson = {
			"status":200,
			"msg":"Sentence saved successfully"
		}
		return jsonify(retJson)


class Get(Resource):
	def post(self):
		#Step 1: Get posted data by the user:
		postedData = request.get_json()

		#Step 2: Read the data:	
		username = postedData["username"]
		password = postedData["password"]

		#Step 3: Verify the username and pw match:
		correct_pw = verifyPw(username, password)

		if not correct_pw:
			retJson = {
				"status":302
			}
			return jsonify(retJson)

		#Step 4: Verify if user has enough tokens:
		num_tokens = countTokens(username)

		if num_tokens <= 0:
			retJson = {
				"status":301
			}
			return jsonify(retJson)

		#Make the user pay:
		users.update({
				"Username":username
		}, {
			"$set":{
				"Tokens":num_tokens-1
				}
		})

		sentence = users.find({
			"Username":username

			})[0]["Sentence"]

		retJson = {
			"status":200,
			"sentence": sentence
		}
		return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')	
api.add_resource(Get, '/get')


if __name__=="__main__":
	app.run(host='0.0.0.0')


'''from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import os

app = Flask(__name__)
api = Api(app)


client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
	'num_of_users':0
	})

class Visit(Resource):
	def get(self):
		prev_num = UserNum.find({})[0]['num_of_users']
		new_num = prev_num + 1
		UserNum.update({}, {"$set":{"num_of_users":new_num}})
		return str("Hey u " + str(new_num))


def checkPostedData(postedData, functionName):
	if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
		if "x" not in postedData or "y" not in postedData:
			return 301 #Missing parameters
		else:
			return 200 #Everything is okay
	elif (functionName == "division"):
		if "x" not in postedData or "y" not in postedData:
			return 301
		elif (postedData["y"]) == 0:
			return 302
		else:
			return 200


class Add(Resource):
	def post(self):
		#if I'm here, then the resource Add was requested using the method POST
		
		#Step 1: Get posted data:
		postedData = request.get_json()

		#Step 1b: Verify validity of posted data
		status_code = checkPostedData(postedData, "add")
		if (status_code != 200):
			retJson = {
				"Message": "An err has happened",
				"Status Code": status_code
			}
			return jsonify(retJson)

		#If I'm here, then status_code == 200
		x = postedData["x"]
		y = postedData["y"]
		x = int(x)
		y = int(y)

		#Step 2: Add the posted data:
		ret = x+y
		retMap = {
			'Message': ret,
			'Status Code': 200
		}
		return jsonify(retMap)

class Subtract(Resource):
	def post(self):
		#if I'm here, then the resource Subtract was requested using the method POST
		
		#Step 1: Get posted data:
		postedData = request.get_json()

		#Step 1b: Verify validity of posted data
		status_code = checkPostedData(postedData, "subtract")
		if (status_code != 200):
			retJson = {
				"Message": "An err has happened",
				"Status Code": status_code
			}
			return jsonify(retJson)

		#If I'm here, then status_code == 200
		x = postedData["x"]
		y = postedData["y"]
		x = int(x)
		y = int(y)

		#Step 2: Subtract the posted data:
		ret = x-y
		retMap = {
			'Message': ret,
			'Status Code': 200
		}
		return jsonify(retMap)


class Multiply(Resource):
	def post(self):
		#if I'm here, then the resource Multiply was requested using the method POST
		
		#Step 1: Get posted data:
		postedData = request.get_json()

		#Step 1b: Verify validity of posted data
		status_code = checkPostedData(postedData, "multiply")
		if (status_code != 200):
			retJson = {
				"Message": "An err has happened",
				"Status Code": status_code
			}
			return jsonify(retJson)

		#If I'm here, then status_code == 200
		x = postedData["x"]
		y = postedData["y"]
		x = int(x)
		y = int(y)

		#Step 2: Multiply the posted data:
		ret = x*y
		retMap = {
			'Message': ret,
			'Status Code': 200
		}
		return jsonify(retMap)



class Divide(Resource):
	def post(self):
		#if I'm here, then the resource Divide was requested using the method POST
		
		#Step 1: Get posted data:
		postedData = request.get_json()

		#Step 1b: Verify validity of posted data
		status_code = checkPostedData(postedData, "division")
		if (status_code != 200):
			retJson = {
				"Message": "An err has happened",
				"Status Code": status_code
			}
			return jsonify(retJson)

		#If I'm here, then status_code == 200
		x = postedData["x"]
		y = postedData["y"]
		x = int(x)
		y = int(y)

		#Step 2: Divide the posted data:
		ret = (x*1.0)/y
		retMap = {
			'Message': ret,
			'Status Code': 200
		}
		return jsonify(retMap)

	
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
	return "Keep studding MotherFucker, Portugal is waiting you!"


if __name__=="__main__":
	app.run(host='0.0.0.0')
'''	