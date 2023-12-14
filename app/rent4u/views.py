from flask import Blueprint,render_template

rent4u = Blueprint('rent4u', __name__)

@rent4u.route('/')
@rent4u.route('/index')
@rent4u.route('/home')
def index():
    return render_template('index.html', is_home_page=True)

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