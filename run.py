from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import utils.responses as responses
<<<<<<< HEAD
from utils.responses import *
from utils.hashing import *
from utils.config import *
=======
from warrant import Cognito
from utils.responses import *
from utils.hashing import *
from utils.config import *
import decimal
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006
import json
import decimal
import socket
import uuid
import datetime
from keys import Keys
<<<<<<< HEAD
from config import *


<<<<<<< HEAD
=======

INITIALSETUP()
=======
from TwitterAPI import TwitterAPI
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006

>>>>>>> 06fc9a658d574f5c231dc460b5bec680a5e060b1
app = Flask(__name__)

session = Session(
<<<<<<< HEAD
<<<<<<< HEAD
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION"]
=======
	aws_access_key_id = Keys.AWS_ACCESS_KEY,
	aws_secret_access_key = Keys.AWS_SECRET_KEY,
	region_name = "us-east-2"
>>>>>>> 21f262554d08eaed42c89c8e8caa54805cec615a
=======
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION_NAME"]
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006
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

<<<<<<< HEAD
@app.route("/testdate")
def testdate():
	hireDate = "1/1/2018";
	hireDate_dt_obj = datetime.datetime.strptime(hireDate,'%m/%d/%Y')
	return dt_obj.month;

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
=======
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
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006

<<<<<<< HEAD
@app.route('/createEmployee', methods=['POST'])
=======
@app.route('/api/create',methods=['GET', 'POST'])
>>>>>>> 21f262554d08eaed42c89c8e8caa54805cec615a
def create():
<<<<<<< HEAD
<<<<<<< HEAD
	loadMe = json.dumps(request.form)
	payInfo = json.loads(loadMe)
	try:
		uuid = generate_uuid(payInfo);
		response = table.put_item(
			Item={
				'userID' : uuid, #PRIMARY KEY
				'name': payInfo["name"],
				'email' : payInfo["email"],
				'password' : sha256encrypt(payInfo["password"]),
				'hireDate': payInfo["hireDate"], #format: MM/DD/YYYY
				'department': payInfo["department"],
				'salary' : int(payInfo["salary"]),
				'admin' : int(payInfo["adminStatus"]) #0 if reg user, 1 if admin
			}
		)
	except Exception as e:
		return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={"value" : str(e)});
	else:
		return response_with(responses.SUCCESS_200, value={"value" : uuid})


#deploy to heroku
#implement cognito
#getwholetable
#deleteEmployee

#request time off (Form) -> notifies admin, admin approves

#total paid time off available
#---vacation history
#------new row

@app.route('/employeeSignIn', methods=['POST'])
def employeeSignIn():
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
		return response_with(responses.SUCCESS_200, value={"value" : dumpedItem});

=======
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
=======
		loadMe = json.dumps(request.get_json(silent=True)["info"])
		payInfo = json.loads(loadMe)
		admin = payInfo["admin"]
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006

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

@app.route('/api/getTable', methods=['GET'])
def getWholeTable():
		info=[]
		response = table.scan()
<<<<<<< HEAD
		for i in response['Items']:
			info.append(json.dumps(i, cls=DecimalEncoder))
		return (jsonify(info))
>>>>>>> 06fc9a658d574f5c231dc460b5bec680a5e060b1

<<<<<<< HEAD
# @app.route('/query')
# def query():
# 	response = table.query( #doesnt work properly
# 		KeyConditionExpression=Key('Salary').eq(100000)
# 	)
=======
@app.route('/api/query')
def query():
	response = table.query( #doesnt work properly
		KeyConditionExpression=Key('Salary').eq(100000)
	)
>>>>>>> 21f262554d08eaed42c89c8e8caa54805cec615a

# 	return (jsonify(response['Items']))
=======
		item = response["Items"]
		# for i in response['Items']:
		# 	info.append(json.dumps(i, cls=DecimalEncoder))
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
		return response_with(responses.SUCCESS_200, value={"value" : dumpedItem })

def getTable():
		response = table.scan()
		item = response["Items"]
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
		return dumpedItem
>>>>>>> 46d994e0250be8afa1ce1cdfd787b99d57263006

@app.route('/api/login',methods=['POST'])
def login():

	loadMe = json.dumps(request.get_json(silent=True)["user"])
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
	timeoffInfo = json.loads(json.dumps(request.get_json()["info"]))
	print(timeoffInfo)
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

@app.route('/api/getTimeOffTable', methods=['GET'])
def getTimeOffTable():
		response = timeOffTable.scan()
		item = response["Items"]
		# for i in response['Items']:
		# 	info.append(json.dumps(i, cls=DecimalEncoder))
		dumpedItem = json.loads(json.dumps(item, default=decimal_default));
		return response_with(responses.SUCCESS_200, value={"value" : dumpedItem })

@app.route('/api/oneUserTimeOff', methods=['GET'])
def oneUserTimeOff():
	userID = request.args.get("userID")
	print(userID)
	fe = Key('userID').eq(userID)
	response = timeOffTable.scan( FilterExpression = fe )
	item = response["Items"]
	convertedItem = json.loads(json.dumps(item, default=decimal_default))
	return response_with(responses.SUCCESS_200, value={"value":convertedItem})

@app.route('/api/acceptrequest', methods=['POST'])
def accept_request():
	timeoffInfo = json.loads(json.dumps(request.get_json()["info"]))
	try:
		response = timeOffTable.update_item(
			Key= {
				"timeoffID" : timeoffInfo["timeoffID"]
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
	timeoffInfo = json.loads(json.dumps(request.get_json()["info"]))
	try:
		response = timeOffTable.update_item(
			Key= {
				"timeoffID" : timeoffInfo["timeoffID"]
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
