import os
from flask import Blueprint, flash, redirect,render_template, request, send_from_directory, url_for


rent4u = Blueprint('rent4u', __name__)

@rent4u.route('/')
@rent4u.route('/index')
@rent4u.route('/home')
def index():
    form= SearchForm()
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
from app.rent4u.models import Car, CarForm, SearchForm
from werkzeug.utils import secure_filename

@rent4u.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print("AAAAA")
    cars=Car.query.all()
    return render_template('search.html',form=form, cars=cars)
    # return redirect(url_for('rent4u.index'))

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
            year=form.year.data,
            color=form.color.data,
            license_plate=form.license_plate.data,
            availability= form.availability.data == 'available',
            current_location=form.current_location.data,
            rental_rate=form.rental_rate.data,
            description=form.description.data,
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