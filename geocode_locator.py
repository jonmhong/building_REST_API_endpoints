import httplib2
import json


google_api_key = "AIzaSyANbOmmApPNwoUOJ_u1q4MnohifOsMAO9A"

def get_geocode_location(inputString):
	global google_api_key
	locationString = inputString.replace(" ", "+")
	url = ("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (locationString, google_api_key))
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result_data = json.loads(content)
	lat = result_data['results'][0]['geometry']['location']['lat']
	lng = result_data['results'][0]['geometry']['location']['lng']

	return (lat, lng)
