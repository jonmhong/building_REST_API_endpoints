from models import Base, User, LinkedIn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from flask import Flask, jsonify, request, url_for, abort, g
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(username=username).first()
	if not user or not user.verify_password(password):
		print "Incorrect user or password"
		return False
	else:
		g.user = user
		return True


@app.route('/users', methods=['POST'])
def add_user():
	user = request.args.get('username', '')
	pw = request.args.get('password', '')

	if user is None or pw is None:
		raise Exception("Please enter both a username and password")

	if session.query(User).filter_by(username=user).first() is not None:
		raise Exception("Username already exists")

	new_user = User(username=user)
	new_user.hash_password(pw)
	session.add(new_user)
	session.commit()
	return jsonify({'username': new_user.username})


@app.route('/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(username=id).one()
	if not user:
		abort(400)
	return jsonify({'username': user.username})


@app.route('/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s' % g.user.username})


@app.route('/linkedin', methods=['GET', 'POST'])
@auth.login_required
def show_linkedin():
	if request.method == 'GET':
		linkedin = session.query(LinkedIn).all()
		return jsonify([l.serialize for l in linkedin])
	elif request.method == 'POST':
		get_name = request.json.get('name')
		get_link = request.json.get('link')
		get_description = request.json.get('description')

		new_linkedin = LinkedIn(name=get_name, link=get_link, description=get_description)
		session.add(new_linkedin)
		session.commit()
		return jsonify(new_linkedin.serialize)


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)