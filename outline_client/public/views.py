from flask import jsonify, Blueprint, redirect, url_for
from flask_login import current_user, logout_user
from client.libs.core import User, Session
from client import login_manager
import functools
from outline_client.libs.outline import Outline

# setup Blueprint
public = Blueprint('public', __name__)

# Login utilities

def anonymous_required(f):
	"""Require anonymous - otherwise, redirect to private sphere"""
	@functools.wraps(f)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated():
			return redirect(url_for('admin.home'))
		return f(*args, **kwargs)
	return wrapper


@login_manager.user_loader
def load_user(access_token):
	"""Loading a user from saved userId"""
	session = Session(access_token=access_token).get()
	user = User(id=session.user, access_token=access_token).get()
	session.user = user
	if user.is_active():
		return user
	else:
		return None


@login_manager.unauthorized_handler
def unauthorized():
	"""Where unauthenticated users are sent"""
	return redirect(url_for('public.login'))


@public.route('/logout')
def logout():
	"""Logout the user"""
	logout_user()
	return redirect(url_for('public.login'))


# Views
@public.route('/')
def home():
	"""Displays all outlines"""
	outlines = Outline().fetch()
	return jsonify(dict(results=outlines))


@public.route('/login')
@anonymous_required
def login():
	"""Redirects to Braiiin core login"""
	pass


@public.route('/register')
@anonymous_required
def register():
	"""Redirects to Braiiin core registration"""
	pass
