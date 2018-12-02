from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import utils.responses as responses
from warrant import Cognito
from utils.responses import *
from utils.hashing import *
from utils.config import *
import decimal
import json
import socket
import uuid


app = Flask(__name__)

session = Session(
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION_NAME"]
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('172PayrollTable')
client_id = "1htd916grmnak53cvvq3cnsnjq";
pool_id = "us-east-2_kugcHNMgX";

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

@app.route('/cognito/signup')
def cognito_signup():
	email = "sdads@gmail.com"
	password = "Password1"
	u = Cognito(pool_id, client_id, user_pool_region="us-east-2", access_key=os.environ["AWS_ACCESS_KEY"],
				secret_key=os.environ["AWS_SECRET_KEY"]);

	u.add_base_attributes(email=email, name="jon");
	res = u.register(email, password);
	return response_with(responses.SUCCESS_200, value=res)

@app.route('/cognito/login')
def cognito_login():
	try:
		email = "jonlikesapples@gmail.com"
		password = "Password1"
		u = Cognito(pool_id, client_id, user_pool_region="us-east-2", access_key=os.environ["AWS_ACCESS_KEY"],
					secret_key=os.environ["AWS_SECRET_KEY"], username=email);
		u.authenticate(password=password);
		userResponse = {
				"username" : u.username,
				"id_token" : u.id_token,
				"access_token" : u.access_token,
				"refresh_token" : u.refresh_token,
				"token_type" : u.token_type
		}
		return response_with(responses.SUCCESS_200, value=userResponse)
	except Exception as e:
		return response_with(responses.UNAUTHORIZED_403, value={"value" : e.args})

@app.route('/cognito/logout', methods=['POST'])
def cognito_logout():
	try:
		access_token = json.loads(json.dumps(request.form))["access_token"]
		u = Cognito(pool_id, client_id, user_pool_region="us-east-2", access_key=os.environ["AWS_ACCESS_KEY"],
					secret_key=os.environ["AWS_SECRET_KEY"], access_token=access_token);
		u.logout();
		userResponse = {
				"username" : u.username,
				"id_token" : u.id_token,
				"access_token" : u.access_token,
				"refresh_token" : u.refresh_token,
				"token_type" : u.token_type
		}
		return response_with(responses.SUCCESS_200, value=userResponse);
	except Exception as e:
		return response_with(resp.SERVER_ERROR_500, error=e.args);
	return access_token;

@app.route('/api/create',methods=['GET', 'POST'])
def create():
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
