from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bd = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = b"'\xb2\xfe\x86T:\xd0\x8b\x94MI\xe3$\xc4\xd5\x0c"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD/db.sqlite'

    bd.init_app(app)

    from .models import Empresa, Usuario, Proyecto, Historia

    login_manager = LoginManager()
    login_manager.login_view = 'auth.entrar'
    login_manager.login_message = "Se necesita estar autenticado para acceder a esta página"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
