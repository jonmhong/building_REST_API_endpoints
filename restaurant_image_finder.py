import httplib2 # http client library
import json # converting in-memory python objects into json
import sys
import codecs
from geocode_locator import get_geocode_location

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stdout)

def findARestaurant(mealType, location):
	global client_id
	global client_secret
	lat, lng = get_geocode_location(location)

	foursquare_url = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s" % (client_id, client_secret, lat, lng, mealType)
	h = httplib2.Http()
	response, content = h.request(foursquare_url, 'GET')
	api_data = json.loads(content)

	print mealType, location
	print response
	print api_data


	if api_data['response']['venues']:
		restaurant = api_data['response']['venues'][0]
		venue_id = restaurant['id']
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		address = ""
		for i in restaurant_address:
			address += i + " "
		restaurant_address = address

		url = 'https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % (venue_id, client_id, client_secret)

		content_str = h.request(url, 'GET')[1]
		content = json.loads(content_str)

		if content['response']['photos']['items']:
			content = content['response']['photos']['items'][0]
			prefix = content['prefix']
			suffix = content['suffix']
			image_url = prefix + '300x300' + suffix
		else:
			# else input random image of burger
			image_url = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': image_url}
		print "Restaurant Name: %s" % restaurant_info['name']
		print "Restaurant Address: %s" % restaurant_info['address']
		print "Image: %s" % restaurant_info['image']

	else:
		return "No Restaurants Found"


restaurants = {"Burmese": "San Francisco, California",
			   "Pizza": "Tokyo, Japan",
			   "Tacos": "Jakarta, Indonesia",
			   "Tapas": "Maputo, Mozambique",
			   "Falafel": "Cairo, Egypt",
			   "Spaghetti": "New Delhi, India",
			   "Cappuccino": "Geneva, Switzerland",
			   "Sushi": "Los Angeles, California",
			   "Steak": "La Paz, Bolivia",
			   "Gyros": "Sydney, Australia"}

if __name__ == "__main__":
	for k, v in restaurants.iteritems():
		print findARestaurant(k, v)
