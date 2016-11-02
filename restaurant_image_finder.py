import httplib2 # http client library
import json # converting in-memory python objects into json
import sys
import codecs
from geocode_locator import get_geocode_location


client_id = "AYK0HLOF0SGPJGKMDWJDXBWN2VE55DY2UIH1UV4CF0TXRJC4"
client_secret = "Y31ZKBXCOICMWNY1LCRT4G5DS2TTY14TII0P4HR3PMEGH3PN"


def findARestaurant(mealType, location):
	global client_id
	global client_secret
	lat, lng = get_geocode_location(location)

	foursquare_url = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s" % (client_id, client_secret, lat, lng, mealType)
	h = httplib2.Http()
	response, result = h.request(foursquare_url, 'GET')
	api_data = json.loads(result)

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

		_, content_str = h.request(url, 'GET')
		content = json.loads(content_str)

		if content['response']['photos']['items']:
			content = content['response']['photos']['items'][0]
			prefix = content['prefix']
			suffix = content['suffix']
			image_url = prefix + '300x300' + suffix
		else:
			# else input random image of burger
			restaurant_image = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': restaurant_image}
		return restaurant_info

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
