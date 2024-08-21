from flask import Flask
from config.config import Config
from application.routes.auth_routes import auth_bp
from application.routes.user_routes import user_bp

from application.routes.profile_routes import profile_bp
from application.routes.permission_routes import permission_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    # Registro dos blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(permission_bp)

    # Listar as rotas registradas
    with app.app_context():
        print(app.url_map)

    return app
