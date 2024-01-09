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

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

csrf = CSRFProtect(app)
csrf.init_app(app)
app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


from app.auth import AdminModelView, MyAdminIndexView, UserModelView, CustomerModelView, CarModelView, ReservationAdminView
from app.auth.models import User
from app.rent4u.models import Customer, Car, Location, Reservation
    
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(UserModelView(User, db.session))
admin.add_view(CustomerModelView(Customer, db.session))
admin.add_view(CarModelView(Car, db.session))
admin.add_view(AdminModelView(Location, db.session))
admin.add_view(ReservationAdminView(Reservation, db.session))
# admin.add_view(ModelView(Invoice, db.session))


from app.auth.views import auth
app.register_blueprint(auth)

from app.rent4u.views import rent4u
app.register_blueprint(rent4u)

ctx = app.app_context()

ctx.push()
from app.auth.models import User
from app.rent4u.models import Car, Location, Reservation
# Reservation.__table__.drop(db.engine)
db.create_all()
# Invoice.__table__.drop(db.engine)
ctx.pop()