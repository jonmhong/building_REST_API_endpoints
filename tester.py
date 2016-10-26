import httplib2
import sys
import json

import codecs

# print debugging information
# change from ascii to utf8
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print "Running Engpoint Tester...\n"
address = raw_input("Enter the address of the server you want to access,\nIf left blank the connection will be set to http://localhost:5000: ")
if address == '':
	address = 'http://localhost:5000'

# First Test (of 5)
try:
	print "Test 1: Creating new Restaurants..."
	url = address + '/restaurants?location=Buenos+Aires+Argentina&mealType=Sushi'
	h = httplib2.Http()
	response, result = h.request(url, 'POST')

	# refer to: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
	if response['status'] != '200': # the satus code class of 2xx means successful
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print json.loads(result)

	url = address + '/restaurants?location=Denver+Colorado&mealType=Soup'
	h = httplib2.Http()
	response, result = h.request(url, 'POST')

	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print json.loads(result)

	url = address + '/restaurants?location=Prague+Czech+Republic&mealType=Crepes'
	h = httplib2.Http()
	response, result = h.request(url, 'POST')

	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print json.loads(result)

	url = address + '/restaurants?location=Shanghai+China&mealType=Sandwiches'
	h = httplib2.Http()
	response, result = h.request(url, 'POST')

	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print json.loads(result)

	url = address + '/restaurants?location=Nairobi+Kenya&mealType=Pizza'
	h = httplib2.Http()
	response, result = h.request(url,'POST')

	if response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])
	print json.loads(result)

except Exception as err:
	print "Test 1 FAILED: Could not add new restaurants"
	print err.args
	sys.exit()

else:
	print "Test 1 PASS: Successfully Made all new restaurants"


# Second Test

