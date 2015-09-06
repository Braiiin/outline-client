# the main Flask application
from outline_client import create_outline_app

app = create_outline_app(root='outline_client')

if __name__ == "__main__":
	app.run(**app.config['INIT'])
