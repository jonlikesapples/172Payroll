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
from keys import Keys
from TwitterAPI import TwitterAPI

app = Flask(__name__)

session = Session(
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION_NAME"]
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('172PayrollTable')
timeOffTable = dynamodb.Table('172TimeOffTable')
client_id = os.environ["COGNITO_CLIENT_ID"];
pool_id = os.environ["COGNITO_POOL_ID"]

consumer_key = os.environ["consumer_key"]
consumer_secret = os.environ["consumer_secret"]
access_token_key = os.environ["access_token_key"]
access_token_secret = os.environ["access_token_secret"]

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

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
		loadMe = json.dumps(request.get_json(silent=True)["info"])
		payInfo = json.loads(loadMe)
		admin = payInfo["admin"]

		u = Cognito(pool_id, client_id, user_pool_region="us-east-2", access_key=os.environ["AWS_ACCESS_KEY"],
				secret_key=os.environ["AWS_SECRET_KEY"]);
		u.add_base_attributes(email=payInfo["email"], name="name");
		#email has to be proper email format
		#password needs to have uppercase, lowercase, and a number
		res = u.register(payInfo["email"], payInfo["password"]);

		try:
			uuid = generate_uuid(payInfo)
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

def getTable():
		response = table.scan()
		item = response["Items"]
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
		return dumpedItem;

@app.route('/api/login',methods=['POST'])
def login():

	loadMe = json.dumps(request.form)
	payInfo = json.loads(loadMe)
	try:

		u = Cognito(pool_id, client_id, user_pool_region='us-east-2',
                    access_key=os.environ["AWS_ACCESS_KEY"], secret_key=os.environ['AWS_SECRET_KEY'],
                    username=payInfo["email"]);
		u.authenticate(password=payInfo["password"]);
		uuid = generate_uuid(payInfo)
		response = table.get_item(
			Key={
				'userID' : uuid
			}
		)
		item = response['Item'];
		# return jsonify(item);
		convertedItem = json.loads(json.dumps(item, default=decimal_default));
		adminStatus = convertedItem['admin'];
		wholeTable = getTable();
		if (adminStatus == 1):
			return response_with(responses.SUCCESS_200, value={"value" : wholeTable}, message={"userID" : uuid, "admin" : adminStatus});
		elif (adminStatus == 0): #just a reg employee
			return response_with(responses.SUCCESS_200, value={"value": convertedItem}, message={"userID" : uuid, "admin" : adminStatus}); #returns just user

	except Exception as e:
		return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})

@app.route('/api/twitter',methods=["POST"])
def twitter():
	TWEET_TEXT = request.get_json()['text']
	r = api.request('statuses/update', {'status': TWEET_TEXT})
	print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
	return str(r.status_code)

@app.route('/api/delete', methods=['DELETE'])
def delete():
   loadMe = json.dumps(request.get_json()["id"])
   payInfo = json.loads(loadMe)
   try:
       response = table.delete_item(
           Key={
               'userID' : payInfo
           }
       )
       response = json.loads(json.dumps(response))
   except Exception as e:
       return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})
   else:
       return response_with(responses.SUCCESS_200, value={"value": response});

@app.route('/api/requesttimeoff', methods=['POST'])
def request_time_off():
	timeoffInfo = json.loads(json.dumps(request.form))
	#columns
	#timeoffid, userid, start date, enddate, status (0,1,2)
	try:
		response = timeOffTable.put_item(
			Item = {
				"timeoffID" : generate_vacation_uuid(timeoffInfo),
				"userID" : timeoffInfo["userID"],
				"startDate" : timeoffInfo["startDate"],
				"endDate" : timeoffInfo["endDate"],
				"timeStatus" : 2
			}
		)
	except Exception as e:
		return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})
	else:
		return response_with(responses.SUCCESS_200, value={"value" : "yay"});

@app.route('/api/admingetrequests', methods=['GET'])
def admin_get_requests():
	fe = Key('timeStatus').eq(2);
	response = timeOffTable.scan( FilterExpression = fe )
	item = response["Items"]
	convertedItem = json.loads(json.dumps(item, default=decimal_default))
	# return jsonify(convertedItem);
	# return json(response["Items"])
	return response_with(responses.SUCCESS_200, value={"value":convertedItem})

@app.route('/api/acceptrequest', methods=['POST'])
def accept_request():
	timeoffInfo = json.loads(json.dumps(request.form))
	try:
		response = timeOffTable.update_item(
			Key= {
				"timeoffID" : generate_vacation_uuid(timeoffInfo)
			},
			UpdateExpression="set timeStatus = :val",
			ExpressionAttributeValues={
				':val': decimal.Decimal(1)
			},
			ReturnValues="ALL_NEW"
		)
		requestResp = json.loads(json.dumps(response, default=decimal_default));
	except Exception as e:
		return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})
	else:
		return response_with(responses.SUCCESS_200, value={"value": requestResp});

@app.route('/api/rejectrequest', methods=['POST'])
def reject_request():
	timeoffInfo = json.loads(json.dumps(request.form))
	try:
		response = timeOffTable.update_item(
			Key= {
				"timeoffID" : generate_vacation_uuid(timeoffInfo)
			},
			UpdateExpression="set timeStatus = :val",
			ExpressionAttributeValues={
				':val': decimal.Decimal(0)
			},
			ReturnValues="ALL_NEW"
		)
		requestResp = json.loads(json.dumps(response, default=decimal_default));
	except Exception as e:
		return response_with(responses.UNAUTHORIZED_401, value={"value" : str(e)})
	else:
		return response_with(responses.SUCCESS_200, value={"value": requestResp});

if __name__ == '__main__':
	app.debug = True
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
	app.run(threaded=True)
