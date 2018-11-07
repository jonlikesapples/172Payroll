from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json
import socket
import uuid
from keys import Keys
from config import *



INITIALSETUP();

app = Flask(__name__)

session = Session(
	aws_access_key_id = Keys.AWS_ACCESS_KEY,
	aws_secret_access_key = Keys.AWS_SECRET_KEY,
	region_name = Keys.AWS_REGION
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('172PayrollTable')

@app.route('/')
def hello_world():
	return "hello world"


@app.route('/create')
def create():
		first_name = request.args.get("firstname")
		last_name = request.args.get("lastname")
		salary = request.args.get("salary")
		if first_name is None or last_name is None or salary is None:
			return "Something is left empty!";
		response = table.put_item(
			Item={
				'userID' : str(uuid.uuid1()), #PRIMARY KEY
				'FirstName': first_name,
				'LastName': last_name,
				'Salary': salary,
			}
		)
		return (jsonify(response));

@app.route('/query')
def query():
	response = table.query( #doesnt work properly
		KeyConditionExpression=Key('Salary').eq(100000)
	)

	return (jsonify(response['Items']))

if __name__ == '__main__':
	app.debug = True
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
	app.run(threaded=True)
