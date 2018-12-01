from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import utils.responses as responses
from utils.responses import *
from utils.hashing import *
from utils.config import *
import decimal
import json
import socket
import uuid
from keys import Keys
from config import *


app = Flask(__name__)

session = Session(
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION"]
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

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError

@app.route('/api/')
def hello_world():
	return "hello world"

@app.route('/api/create',methods=['GET', 'POST'])
def create():
		# name = request.args.get("name")
		# salary = request.args.get("salary")
		# email = request.args.get("email")
		# hireDate = request.args.get("hireDate")
		# department = request.args.get("department")
		# if name is None or salary is None or email is None or hireDate is None or department is None:
		# 	return "Something is left empty!"
		loadMe = json.dumps(request.form)
		payInfo = json.loads(loadMe)
		admin = payInfo["admin"]
		try:
			uuid = generate_uuid(payInfo);
			response = table.put_item(
				Item={
					'userID' : uuid,
					'name': payInfo["name"],
					'email': payInfo["email"],
					'password': sha256encrypt(payInfo["password"]),
					'hireDate' : payInfo["hireDate"], #format: MM/DD/YYYY
					'department' : payInfo["department"],
					'salary' : int(payInfo["salary"]),
					'admin' :int(admin)
				}
			)
		except Exception as e:
			return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={"value" : str(e)});
		else:
			return response_with(responses.SUCCESS_200, value={
				"userID" : uuid,
				"admin" : int(admin)
			})

@app.route('/api/getTable', methods=['GET'])
def getTable():
		info=[]
		response = table.scan()
		item = response["Items"]
		# for i in response['Items']:
		# 	info.append(json.dumps(i, cls=DecimalEncoder))
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
		return response_with(responses.SUCCESS_200, value={"value" : dumpedItem })

@app.route('/api/login',methods=['POST'])
def login():
	loadMe = json.dumps(request.form)
	payInfo = json.loads(loadMe)
	try:
		uuid = generate_uuid(payInfo)
		response = table.get_item(
			Key={
				'userID' : uuid
			}
		)
		item = response['Item'];
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
	except Exception as e:
		return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})
	else:
		return response_with(responses.SUCCESS_200, value={"value": dumpedItem});

if __name__ == '__main__':
	app.debug = True
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
	app.run(threaded=True)
