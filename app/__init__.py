from flask import Flask, jsonify
from os.path import join, dirname, realpath
from flask_login import LoginManager

# SQLAlchemy for database creation and updating
from flask_migrate import Migrate

'''App factory'''
# initialising flask app and path to database
def create_app():
	app = Flask(__name__)

	app.config.from_object('app.config.DevelopmentConfig')

	UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	from app.models import db, User
	db.init_app(app)
	# to handle adding or removing of columns of already created DB
	migrate = Migrate(app, db)

	@app.route('/ping', methods=['GET'])
	def ping_pong():
		return jsonify({
			'status': 'Epic success',
			'message': 'pong!'
			})
    
	from app.admin_views import admin
	from app.login_views import login
	from app.views import base

	'''Log-in manager initialisation'''
	# initalising login manager
	login_manager = LoginManager()
	login_manager.init_app(app)
	# link to log in page
	login_manager.login_view = "login.logIn"
 
	''' Misc and Error Handling'''
	# user loader to remember previously visited users
	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))
 
	app.register_blueprint(admin)
	app.register_blueprint(login)
	app.register_blueprint(base)
 
	# return app
	return app
