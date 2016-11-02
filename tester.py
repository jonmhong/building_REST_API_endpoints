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

# POST Test
try:
	print "Test 1: Creating new Restaurants..."
	url = address + '/restaurants?location=Buenos+Aires+Argentina&mealType=Sushi'
	h = httplib2.Http()
	response, result = h.request(url, 'POST')

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


# GET Test
try:
	print "Attempting Test 2: Reading all Restaurants: "
	url = address + "/restaurants"
	h = httplib2.Http()
	response, result = h.request(url, 'GET')
	if response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])
	json_result = json.loads(result)
	print json_result

except Exception as err:
	print "Test 2 FAILED: Could not find any restaurants"
	print err.args

else:
	print "Test 2 PASS: Successfully made all new restaurants"


# Specific Restaurant GET Test
try:
	print "Attempting Test 3: Reading a specific restaurant"
	all_restaurants = json_result
	rest_id = all_restaurants['restaurants'][len(all_restaurants['restaurants']) - 1]['id']
	restaurant_url = address + "/restaurants/%s" % rest_id
	h = httplib2.Http()
	response, result = h.request(restaurant_url, 'GET')
	if response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])
	print json.loads(result)

except Exception as err:
	print "Test 3 FAILED: Could not find specific restaurant with id %s " % rest_id
	print err.args
else:
	print "Test 3 PASS: Successfully made GET request"


# PUT Test
try:
	print "Changing the name, image, and address of the first restaurant in the database"
	h = httplib2.Http()
	rest_id = json_result['restaurants'][0]['id']
	url = address + "/restaurants/%s?name=Udacity&address=2465+Latham+Street+Mountain+View+CA&image=https://media.glassdoor.com/l/70/82/fc/e8/students-first.jpg" % rest_id

	response, result = h.request(url, 'PUT')

	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print json.loads(result)

except Exception as err:
	print "Test 4 FAILED: Couldn't update restaurant from server"
	print err.args
else:
	print "Test 4 PASS: Successfully updated first restaurant"


# DELETE Test
try:
	print "Attempting Test 5: Deleting the second restaurant from the server"
	rest_id = json_result['restaurants'][1]['id']
	url = address + "/restaurants/%s" % rest_id
	h = httplib2.Http()
	response, result = h.request(url, 'DELETE')
	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])
	print result

except Exception as err:
	print "Test 5 FAILED: Could not find and delete restaurant from server"
	print err.args
else:
	print "Test 5 PASS: Successfully deleted restaurant from server"
