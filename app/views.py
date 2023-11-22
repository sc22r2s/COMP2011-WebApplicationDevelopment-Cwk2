from flask import render_template, request, redirect, url_for, flash
from app import app, db, admin, models, login_manager
from flask_login import UserMixin, login_user, logout_user

from sqlalchemy.exc import IntegrityError, DataError, OperationalError

from .forms import (LoginForm, SignUpForm)

@login_manager.user_loader
def loader_user(user_id):
	return models.Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = SignUpForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form.get("password") == request.form.get("confirmPassword"):
                    user = models.Users(username=request.form.get("username"),
                            password=request.form.get("password"))
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for("login"))
                else:  # Passwords does not match
                    flash("Passwords does not match", "danger")
            except (IntegrityError, AttributeError):  # Username already exists
                flash("Username already taken", "danger")
    return render_template("sign_up.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = models.Users.query.filter_by(
                username=request.form.get("username")).first()
                if user.password == request.form.get("password"):
                    login_user(user)
                    flash("Logged in successfully", "success")
                    return redirect(url_for("home"))
                else:
                    # Clear form fields
                    form.username.data = ""
                    form.password.data = ""
                    flash("Incorrect username or password", "danger")
            except (IntegrityError, AttributeError):
                # Clear form fields
                form.username.data = ""
                form.password.data = ""
                flash("Incorrect username or password", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")
