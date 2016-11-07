from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)
	password_hash = Column(String(64))

	def hash_password(self, password):
		# hash the password
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		# print True if the password is found in the hash
		return pwd_conext.verify(password, self.password_hash)
	
	
class LinkedIn(Base):
	__tablename__ = 'LinkedIn'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	link  = Column(String)
	description = Column(String)
	
	@property
	def serialize(self):
		return {
			'name': self.name,
			'link': self.link,
			'description': self.description
		}



engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)
