from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
import decimal
from boto3.dynamodb.conditions import Key, Attr
import json
import socket
import uuid
from keys import Keys
from config import *



INITIALSETUP()

app = Flask(__name__)

session = Session(
	aws_access_key_id = Keys.AWS_ACCESS_KEY,
	aws_secret_access_key = Keys.AWS_SECRET_KEY,
	region_name = "us-east-2"
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('172PayrollTable')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

@app.route('/api/')
def hello_world():
	return "hello world"


@app.route('/api/create',methods=['GET', 'POST'])
def create():
		name = request.args.get("name")
		salary = request.args.get("salary")
		email = request.args.get("email")
		hireDate = request.args.get("hireDate")
		department = request.args.get("department")
		if name is None or salary is None or email is None or hireDate is None or department is None:
			return "Something is left empty!"
		response = table.put_item(
			Item={
				'userID' : str(uuid.uuid1()), #PRIMARY KEY
				'name': name,
				'salary': salary,
				'email': email,
				'hireDate' : hireDate,
				'department': department,
			}
		)
		return (jsonify(response))


@app.route('/api/getTable', methods=['GET'])
def getTable():
		info=[]
		response = table.scan()
		for i in response['Items']:
			info.append(json.dumps(i, cls=DecimalEncoder))
		return (jsonify(info))

@app.route('/api/query')
def query():
	response = table.query( #doesnt work properly
		KeyConditionExpression=Key('Salary').eq(100000)
	)

	return (jsonify(response['Items']))

@app.route('/api/login',methods=['GET', 'POST'])
def login():
	username = request.args.get("username")
	password = request.args.get("password")
	print(username)
	print(password)
	response = {
		'code' : 200
	}
	return (jsonify(response))

if __name__ == '__main__':
	app.debug = True
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
	app.run(threaded=True)
