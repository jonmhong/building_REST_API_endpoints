# DONE: 1 Receive username/password login
# 2 Send Serialized, encrypted token with timeframe
# 3 Check if client has sent the correct auth token
# 4 Provide JSON information, while token is active

from models import Base, User, LinkedIn
from urllib2 import urlopen
from httplib2 import Http
import json
import sys
import base64

address = raw_input("Input the server name you want to access,\nIf left blank, connection set to http://localhost:5000:\n")

if address == "":
	address = "http://localhost:5000"


# Test Case 1: Register a New User
try:
	h = Http()
	data = dict(username='jonmhong', password='Hello World!')
	json_data = json.dumps(data)
	url = address + '/users'
	response, result = h.request(url, 'POST', body=json_data, headers={"Content-Type": "application/json"})
	if response['status'] != '200' and response['status'] != '201':
		raise Exception("Received an unsuccessful status request %s" % response['status'])

except Exception as err:
	print "Could not successfully create a new user"
	print err.args

else:
	print "Test 1 PASS"


# Test Case 2: Obtain a Token
try:
	h = Http()
	url = address + '/token'
	h.add_credentials("jonmhong", "Hello World!") # this is login info, when account has already been created
	response, result = h.request(url, 'GET', headers={"Content-Type": "application/json"})
	print result
	result = json.loads(result)
	print result

	if not result:
		raise Exception("No result provided")

	if response['status'] != '200':
		raise Exception("Received connection status of %s" % response['status'])

	if not result['token']:
		raise Exception("Did not receive token")

	print "Received token: %s" % result['token']

except Exception as err:
	print "Test 2 FAILED"
	print err.args

else:
	print "Test 2 PASS: Received Token"


# Test Case 3: Access Endpoint with Invalid Token

# Test Case 4: View JSON information in db

# Test Case 4: Login with Valid Token