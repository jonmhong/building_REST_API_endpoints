# column object, integer, and string objects
from sqlalchemy import Column, Integer, String
# base class for declarative class definitions
from sqlalchemy.ext.declarative import declarative_base
# create a database engine
from sqlalchemy import create_engine

# Create Base declarative class
Base = declarative_base()

# Create child class that inherits Base attributes and functions
class Puppy(Base):
	# set title
	__tablename__ = 'puppy'

	# set 3 columns
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))

	# serialize
	@property
	def serialize(self):
		return {
				 'id': self.id,
				 'name': self.name,
				 'description': self.description
		}



engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)