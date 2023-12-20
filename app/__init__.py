import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)



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



admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
class UserAdminView(ModelView):
    column_exclude_list = ['pwdhash']
    
from app.auth.models import User
from app.rent4u.models import Customer, Car, Rental, Location, Reservation, Invoice
admin.add_view(UserAdminView(User, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Car, db.session))
admin.add_view(ModelView(Rental, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Reservation, db.session))
admin.add_view(ModelView(Invoice, db.session))

from app.auth.views import auth
app.register_blueprint(auth)

from app.rent4u.views import rent4u
app.register_blueprint(rent4u)

ctx = app.app_context()

ctx.push()
from app.auth.models import User
from app.rent4u.models import Car, Rental, Location, Reservation, Invoice
db.create_all()
ctx.pop()