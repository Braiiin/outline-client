import sys
import os
sys.path.insert(0, os.path.join(os.getcwd()+"/client"))

from client import create_app
from outline_client.public.views import public
from outline_client.admin.views import admin

def create_outline_app(**kwargs):
	"""Create a template Flask app"""
	app = create_app(__name__, **kwargs)
	app.register_blueprints(public, admin)
	return app
