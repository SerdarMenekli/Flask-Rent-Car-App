import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)

from app.rent4u.views import rent4u
app.register_blueprint(rent4u)

db_path = os.path.join(app.root_path, 'database', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)
csrf.init_app(app)
app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from app.auth.views import auth
app.register_blueprint(auth)

ctx = app.app_context()

ctx.push()
from app.auth.models import User
from app.rent4u.models import Car, Rental, Location, Reservation, Invoice
db.create_all()
ctx.pop()