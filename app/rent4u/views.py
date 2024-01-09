import os
from flask import Blueprint, flash, redirect,render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required

from app.auth.views import admin_required

rent4u = Blueprint('rent4u', __name__)

@rent4u.route('/')
@rent4u.route('/index')
@rent4u.route('/home')
def index():
    form= SearchForm()
    # if current_user.is_authenticated:
        # print(current_user.username)
        # print(current_user.is_admin())
    return render_template('index.html', is_home_page=True, form=form)

@rent4u.route('/about')
def about():
    return render_template('about.html')

@rent4u.route('/blog')
def blog():
    return render_template('blog.html')

@rent4u.route('/car')
def car():
    return render_template('car.html')

@rent4u.route('/contact')
def contact():
    return render_template('contact.html')

from app import ALLOWED_EXTENSIONS, db, app
from app.rent4u.models import Car, CarForm, Reservation, ReservationForm, SearchForm, Customer
from werkzeug.utils import secure_filename

@rent4u.route('/search', methods=['GET'])
def search():
    form = SearchForm(request.args)
    # if form.validate_on_submit():
    #     print("AAAAA")
    # cars=Car.query.all()
    #products = Product.query.paginate(page=page, per_page=5).items
    
    print(form.pick_up_date)
    
    query = Car.query

    query = query.filter(Car.availability == True)
    
    car_type = request.args.get('type')
    if car_type:
        if not car_type=="any":
            query = query.filter(Car.type == car_type)

    transmission = request.args.get('transmission')
    if transmission:
        if transmission != "both":
            query = query.filter(Car.transmission == transmission)

    seats = request.args.get('seats')
    if seats:
        query = query.filter(Car.seats >= seats)

    luggage = request.args.get('luggage')
    if luggage:
        query = query.filter(Car.luggage >= luggage)

    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    if min_price and max_price:
        query = query.filter(Car.rental_rate.between(min_price, max_price))

    if form.sort_by.data == 'price_ascending':
        query = query.order_by(Car.rental_rate.asc())
    elif form.sort_by.data == 'price_descending':
        query = query.order_by(Car.rental_rate.desc())
    
    
    
    page = request.args.get('page', 1, type=int)
    cars = query.paginate(page=page, per_page=10)
    # print(page)
    return render_template('search.html',form=form, cars=cars)
    # return redirect(url_for('rent4u.index'))

@admin_required
@rent4u.route('/add_car', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    
    if form.validate_on_submit():
        # print(form.image.data)
        # print(request.files.keys())
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        
        new_car = Car(
            type=form.type.data,
            transmission=form.transmission.data,
            seats=form.seats.data,
            brand=form.brand.data,
            model=form.model.data,
            doors=form.doors.data,
            luggage=form.luggage.data,
            # year=form.year.data,
            # color=form.color.data,
            # license_plate=form.license_plate.data,
            availability= form.availability.data == 'available',
            # current_location=form.current_location.data,
            rental_rate=form.rental_rate.data,
            # description=form.description.data,
            image_filename=filename if form.image.data else None
        )

        db.session.add(new_car)
        db.session.commit()

        flash('Car added successfully!', 'success')
        return redirect(url_for('rent4u.add_car'))  # Update this route

    return render_template('add_car.html', form=form)

@rent4u.route('/car_image/<filename>')
def car_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from app import csrf

@rent4u.route('/uploadtest', methods=['GET', 'POST'])
@csrf.exempt
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print(request.files.keys())
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('rent4u.upload_file'))
    return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>

            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''

@login_required
@rent4u.route('/reservation', methods=['GET', 'POST'])
def reservation():
    # customer_id = current_user.customer.id if current_user.is_authenticated else None
    # car_id = request.args.get('car_id')
    # pick_up_date = request.args.get('pick_up_date')
    # return_date = request.args.get('return_date')
    # pick_up_location = request.args.get('pick_up_location')
    # return_location = request.args.get('return_location')
    
    # # car = Car.query.get({"id":car_id})
    # car = Car.query.get_or_404(car_id)
    
    form = ReservationForm()
    
    if form.validate_on_submit():
        car_id = form.car_id.data
        # pick_up_date = form.pick_up_date.data
        # return_date = form.return_date.data
        # pick_up_location = form.pick_up_location.data
        # return_location = form.return_location.data
        reservation = Reservation(
                        customer_id = current_user.customer.id,
                        car_id = form.car_id.data,
                        pick_up_date = form.pick_up_date.data,
                        return_date = form.return_date.data,
                        pick_up_location = form.pick_up_location.data,
                        return_location = form.return_location.data
                        )
        db.session.add(reservation)
        car = Car.query.get_or_404(car_id)
        car.availability = False
        db.session.commit()
        flash('Reservation successful', "success")
        return render_template('reservation.html', car = car, form = form, done=True)
    else:  
        car_id = request.args.get('car_id')
        car = Car.query.get_or_404(car_id)
        form = ReservationForm(request.args)
        return render_template('reservation.html', car = car, form = form)
# pickUpDate=pickUpDate, returnDate=returnDate, pickUpLocation=pickUpLocation, returnLocation=returnLocation

@login_required
@rent4u.route('/reservations', methods=['GET'])
def reservations():
    reservations = Reservation.query.filter_by(customer_id=current_user.customer.id).all()
    # print(current_user.customer.id)
    return render_template('reservations.html', reservations=reservations)