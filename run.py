from flask import Flask, jsonify, request
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
import decimal
from boto3.dynamodb.conditions import Key, Attr
import utils.responses as responses
from utils.responses import *
from utils.hashing import *
from utils.config import *
import json
import decimal
import socket
import uuid
import datetime
from keys import Keys
from config import *


<<<<<<< HEAD
=======

INITIALSETUP()

>>>>>>> 06fc9a658d574f5c231dc460b5bec680a5e060b1
app = Flask(__name__)

session = Session(
<<<<<<< HEAD
	aws_access_key_id = os.environ["AWS_ACCESS_KEY"],
	aws_secret_access_key = os.environ["AWS_SECRET_KEY"],
	region_name = os.environ["AWS_REGION"]
=======
	aws_access_key_id = Keys.AWS_ACCESS_KEY,
	aws_secret_access_key = Keys.AWS_SECRET_KEY,
	region_name = "us-east-2"
>>>>>>> 21f262554d08eaed42c89c8e8caa54805cec615a
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

@app.route("/testdate")
def testdate():
	hireDate = "1/1/2018";
	hireDate_dt_obj = datetime.datetime.strptime(hireDate,'%m/%d/%Y')
	return dt_obj.month;

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

<<<<<<< HEAD
@app.route('/createEmployee', methods=['POST'])
=======
@app.route('/api/create',methods=['GET', 'POST'])
>>>>>>> 21f262554d08eaed42c89c8e8caa54805cec615a
def create():
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


@app.route('/api/getTable', methods=['GET'])
def getTable():
		info=[]
		response = table.scan()
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
