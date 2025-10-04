# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from config import Config 



# db = SQLAlchemy()
# migrate = Migrate()


# def create_app(config_class=Config):
# 	app = Flask(__name__)
# 	app.config.from_object(config_class)

# 	db.init_app(app)
# 	migrate.init_app(app, db)
# 	CORS(app)

# 	from backend.routes import api_bp
# 	app.register_blueprint(api_bp, url_prefix='/api')

# 	return app

from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, migrate, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)

    # register blueprints
    from routes.routes import api_bp
    from routes.auth_routes import auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
