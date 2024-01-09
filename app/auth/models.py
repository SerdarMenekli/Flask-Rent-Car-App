from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import DateField, EmailField, StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, DataRequired, Email
from app import db
from wtforms import BooleanField

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pwdhash = db.Column(db.String())
    email = db.Column(db.String(100), unique=True, nullable=False)
    admin = db.Column(db.Boolean())
    
    customer = db.relationship('Customer', backref='user', uselist=False)
    
    def __init__(self, username, password, email, admin=False):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.admin = admin
        
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
    
    def is_admin(self):
        return self.admin
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
        
class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    address = StringField('Address')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    
class ManageAccountForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])
    username = StringField('Username')
    new_password = PasswordField('New Password', [EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    email = EmailField('Email')

class ManagePersonalForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    address = StringField('Address')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    
