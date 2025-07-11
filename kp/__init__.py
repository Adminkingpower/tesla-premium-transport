from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'BetterSecretNeeded123'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kingpower.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    db.init_app(app)

    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(e):
        return "404 - Page Not Found", 404

    @app.errorhandler(500)
    def internal_error(e):
        return "500 - Internal Server Error", 500

    return app
