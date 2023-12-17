from flask import request, render_template, flash, redirect, url_for, session, Blueprint
from app import db
from app.auth.models import User, RegistrationForm, LoginForm, ManageAccountForm, ManagePersonalForm
from app.rent4u.models import Customer
from flask import g
from flask_login import current_user, login_user, logout_user, login_required
from app import login_manager

auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route("/register", methods=["GET", "POST"])
def register():
    # if session.get('username'):
    if current_user.is_authenticated:
        flash("Your are already logged in.", "info")
        return redirect(url_for("rent4u.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        existing_username = User.query.filter_by(username=form.username.data).first()
        # existing_username = User.query.filter(User.username.like("%" + username + "%")).first()
        if existing_username:
            flash("This username has been already taken. Try another one.", "warning")
            return render_template("register.html", form=form)
        
        email=request.form.get("email")
        existing_email = User.query.filter(User.email.like("%" + email + "%")).first()
        if existing_email:
            flash("This email has been already taken. Try another one.", "warning")
            return render_template("register.html", form=form)
        user = User(username, password, email)
        db.session.add(user)
        db.session.commit()
        
        customer = Customer(user_id=user.id, full_name=form.full_name.data, phone_number=form.phone_number.data, address=form.address.data, date_of_birth=form.date_of_birth.data)
        db.session.add(customer)
        db.session.commit()
        flash("You are now registered. Please login.", "success")
        return redirect(url_for("auth.login"))
    if form.errors:
        flash(form.errors, "danger")
    return render_template("register.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("rent4u.index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        existing_user = User.query.filter_by(username=username).first()
        if not (existing_user and existing_user.check_password(password)):
            flash("Invalid username or password. Please try again.", "danger")
            return render_template("login.html", form=form)
        login_user(existing_user)
        flash("You have successfully logged in.", "success")
        return redirect(url_for("rent4u.index"))

    if form.errors:
        flash(form.errors, "danger")
    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    # if google.authorized:
    #     token = google_blueprint.token["access_token"]
    #     resp = google.post(
    #         "https://accounts.google.com/o/oauth2/revoke",
    #         params={"token": token},
    #         headers={"Content-Type": "application/x-www-form-urlencoded"}
    #     )
    #     # assert resp.ok, resp.text
    #     del google_blueprint.token
        
    logout_user()
    return redirect(url_for("rent4u.index"))


@auth.route("/manage")
@login_required
def manage():
    form1 = ManageAccountForm()
    form2 = ManagePersonalForm()
    user = current_user
    customer = user.customer
    return render_template("manage.html", form1=form1, form2=form2, user=user, customer=customer)

@auth.route("/manage_account", methods=["POST"])
@login_required
def manage_account():
    form = ManageAccountForm()
    if form.validate_on_submit():
        user = current_user
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        if user.check_password(password):
            if user.username != username:
                existing_username = User.query.filter_by(username=form.username.data).first()
                if existing_username:
                    flash("This username has been already taken. Try another one.", "warning")
                    return redirect(url_for("auth.manage"))
                user.username = form.username.data
            
            if form.new_password.data:
                user.set_password(form.new_password.data)
                pass
            
            if user.email != form.email.data:
                existing_email = User.query.filter_by(email=form.email.data).first()
                if existing_email:
                    flash("This email has been already taken. Try another one.", "warning")
                    return redirect(url_for("auth.manage"))
                user.email = form.email.data
        else:
            flash("incorrect password", "warning")
            return redirect(url_for("auth.manage"))
        
        db.session.commit()
        flash("Account information updated successfully", "success")
    if form.errors:
        flash(form.errors, "danger")
    return redirect(url_for("auth.manage"))

@auth.route("/manage_personel", methods=["POST"])
@login_required
def manage_personal():
    form = ManagePersonalForm()
    if form.validate_on_submit():
        user = current_user
        customer = user.customer
        
        customer.full_name = form.full_name.data
        customer.phone_number = form.phone_number.data
        customer.address = form.address.data
        customer.date_of_birth = form.date_of_birth.data
        
        db.session.commit()
        flash("Account information updated successfully", "success")
    if form.errors:
        flash(form.errors, "danger")
    return redirect(url_for("auth.manage"))