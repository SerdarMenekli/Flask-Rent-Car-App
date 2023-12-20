from datetime import datetime
from app import db
from flask_wtf import FlaskForm

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    address = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, user_id, full_name, phone_number, address, date_of_birth):
        self.user_id = user_id
        self.full_name = full_name
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth

class Car(db.Model):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    car_type = db.Column(db.String(50))
    transmission = db.Column(db.String(20))
    seats = db.Column(db.Integer)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    color = db.Column(db.String(20))
    license_plate = db.Column(db.String(15), unique=True, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    current_location = db.Column(db.String(255))
    rental_rate = db.Column(db.Float)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, car_type, transmission, seats, brand, model, year, color, license_plate, availability, current_location, rental_rate, description):
        self.car_type = car_type
        self.transmission = transmission
        self.seats = seats
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.license_plate = license_plate
        self.availability = availability
        self.current_location = current_location
        self.rental_rate = rental_rate
        self.description = description
  
  
"""   
# class Car(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(100))
#     transmission = db.Column(db.String(100))
#     seats = db.Column(db.Integer(100))
#     model = db.Column(db.String(100))
#     price_per_day = db.Column(db.Integer)
#     age = db.Column(db.Integer)
#     status = db.Column(db.String(100))
    
#     # type,transmission,seats,model,price_per_day,age,status
#     def __init__(self, type,transmission,seats,model,price_per_day,age,status="available"):
#         self.type = type
#         self.transmission = transmission
#         self.seats = seats
#         self.model = model
#         self.price_per_day = price_per_day
#         self.age = age
#         self.status = status
        
class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date_given = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.Date, nullable=False)
    location_given = db.Column(db.String(255), nullable=False)
    location_returned = db.Column(db.String(255), nullable=False)
    
    #car_id,date_given,date_returned,location_given,location_returned
    def __init__(self, car_id, date_given, date_returned, location_given, location_returned):
        self.car_id = car_id
        self.date_given = date_given
        self.date_returned = date_returned
        self.location_given = location_given
        self.location_returned = location_returned
"""   

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    rental_start_date = db.Column(db.Date, nullable=False)
    rental_end_date = db.Column(db.Date, nullable=False)
    rental_start_location = db.Column(db.String(255))
    rental_end_location = db.Column(db.String(255))
    total_cost = db.Column(db.Float)
    rental_status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, car_id, rental_start_date, rental_end_date, rental_start_location, rental_end_location, total_cost, rental_status):
        self.user_id = user_id
        self.car_id = car_id
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.rental_start_location = rental_start_location
        self.rental_end_location = rental_end_location
        self.total_cost = total_cost
        self.rental_status = rental_status
        
class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, address, contact_number):
        self.name = name
        self.address = address
        self.contact_number = contact_number

class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    reservation_start_date = db.Column(db.Date, nullable=False)
    reservation_end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, car_id, reservation_start_date, reservation_end_date):
        self.user_id = user_id
        self.car_id = car_id
        self.reservation_start_date = reservation_start_date
        self.reservation_end_date = reservation_end_date
        
class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'), nullable=False)
    amount_due = db.Column(db.Float)
    payment_status = db.Column(db.String(20))  # You might use Enum for predefined statuses
    issued_date = db.Column(db.Date, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, rental_id, amount_due, payment_status, issued_date, due_date):
        self.user_id = user_id
        self.rental_id = rental_id
        self.amount_due = amount_due
        self.payment_status = payment_status
        self.issued_date = issued_date
        self.due_date = due_date
        
class SearchForm(FlaskForm):
    pass