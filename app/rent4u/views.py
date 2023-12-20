from flask import Blueprint, redirect,render_template, url_for


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

from app import db
from app.rent4u.models import SearchForm

@rent4u.route('/search', methods=['POST'])
def search():
    form= SearchForm()
    # return render_template('index.html',is_home_page=True, form=form)
    return redirect(url_for('rent4u.index'))