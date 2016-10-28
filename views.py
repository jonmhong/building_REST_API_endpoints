from restaurant_image_finder import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = 'AYK0HLOF0SGPJGKMDWJDXBWN2VE55DY2UIH1UV4CF0TXRJC4'
foursquare_secret_id = 'Y31ZKBXCOICMWNY1LCRT4G5DS2TTY14TII0P4HR3PMEGH3PN'
google_api_key = 'AIzaSyANbOmmApPNwoUOJ_u1q4MnohifOsMAO9A'

### INSTRUCTIONS ###
# endpoint that takes in a city name and mealtype
# geocodes the location
# finds a nearby restaurant with that mealtype
# stores it in the database
# returns it in the json object
### INSTRUCTIONS ###

# 1 create engine
engine = create_engine('sqlite:///restaurants.db')
# 2 bind metadata to engine
Base.metadata.bind = engine
# 3 create session
DBSession = sessionmaker(bind=engine)
# 4 initialize variable to session
session = DBSession()
# 5 create flask application
app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
	# BUG in GET
	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		return jsonify(restaurants=[i.serialize for i in restaurants])

	elif request.method == 'POST':
		location = request.args.get('location', '')
		mealType = request.args.get('mealtype', '')
		restaurant_info = findARestaurant(mealType, location)

		if restaurant_info != "No Restaurants Found":
			restaurant = Restaurant(restaurant_name=unicode(restaurant_info['name']), 
									restaurant_address=unicode(restaurant_info['address']),
									restaurant_image=restaurant_info['image'])
			session.add(restaurant)
			session.commit()
			return jsonify(restaurant=[restaurant.serialize])
		else:
			return jsonify({"Error: No Restaurants Found for %s in %s" % (mealType, location))


@app.route('/restaurants/<int:id>', methods=['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	restaurant = session.query(Restaurant).filter_by(id=id).one() # query restaurant and return one result or raise exception

	if request.method == 'GET':
		return jsonify(restaurant=restaurant.serialize)

	elif request.method == 'PUT':
		# update a specific restaurant
		address = request.args.get('address')
		image = request.args.get('image')
		name = request.args.get('name')

		if address:
			restaurant.restaurant_address = address
		if image:
			restaurant.restaurant_image = image
		if name:
			restaurant.restaurant_name = name

		session.commit()
		return jsonify(restaurant=restaurant.serialize)

	elif request.method == 'DELETE':
		session.delete(restaurant)
		session.commit()
		return "Restaurant Deleted"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
