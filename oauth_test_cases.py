from models import Base, User, LinkedIn
from urllib2 import urlopen
from httplib2 import Http
import json
import sys
import base64

address = raw_input("Input the server name you want to access,\nIf left blank, connection set to http://localhost:5000:\n")

if address == "":
	address = "http://localhost:5000"


# Test Case 1: Test verification for Google auth code
# collect auth from Google
# pass it to endpoint
# endpoint needs to pass to Google
# then receive token
# pass token to client
try:
	h = Http()
	data = dict(username='jonmhong', password='Hello World!', email='jonmhong@gmail.com')
	h.add_credentials("jonmhong", "Hello World!")
	json_data = json.dumps(data)
	url = address + '/oauth/Google'
	response, result = h.request(url, 'GET', body=json_data, headers={"Content-Type": "application/json"})
	if response['status'] != '200' and response['status'] != '201':
		raise Exception("Received an unsuccessful status request %s" % response['status'])


# Test Case 2: Receive access token from Google

# Test Case 3: Use access token to look up user's email address or create a new user

# Test Case 4: Send access token to client