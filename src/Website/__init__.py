from flask_login.login_manager import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from os import path



db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'KOSSSSA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    WTF_CSRF_SECRET_KEY = "THISISASECRET"

    db.init_app(app)
    csrf = CSRFProtect(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    from .views import views
    from .auth import auth
    from .models import User, design, Orders, Colors, MyModelView, Client


    admin = Admin(app, name='belal', template_mode='bootstrap4')
    admin.add_view(MyModelView(design, db.session))
    admin.add_view(MyModelView(Orders, db.session))
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Client, db.session))
    admin.add_view(MyModelView(Colors, db.session))
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)


    return app

def create_database(app):
    if not path.exists(f'Website/{DB_NAME}'):
        db.create_all(app=app)
        print('Database Created!.')
    pass