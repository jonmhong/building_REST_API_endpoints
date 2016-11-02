# column object, integer, and string objects
from sqlalchemy import Column, Integer, String
# base class for declarative class definitions
from sqlalchemy.ext.declarative import declarative_base
# create a database engine
from sqlalchemy import create_engine

# Create Base declarative class
Base = declarative_base()

# Create child class that inherits Base attributes and functions
class Restaurant(Base):
	# set title
	__tablename__ = 'restaurant sql table' # initialize title

	# set 3 columns
	id = Column(Integer, primary_key=True) # primary_key is a list of column objects
	restaurant_name = Column(String)
	restaurant_address = Column(String)
	restaurant_image = Column(String)

	@property # using the property function can produce modified behavior for an attribute
	# also to serialize information from database
	def serialize(self):
		return {
			'id': self.id,
			'restaurant_name': self.restaurant_name,
			'restaurant_address': self.restaurant_address,
			'restaurant_image': self.restaurant_image
		}


# create an engine instance that indicates database dialect, url is a string
engine = create_engine('sqlite:///restaurants.db')
# metadata subclass
Base.metadata.create_all(engine)
