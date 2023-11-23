from flask import render_template, request, redirect, url_for, flash
from app import app, db, admin, models, login_manager, bcrypt
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from .forms import (LoginForm, SignUpForm, EditAccountForm)

@login_manager.user_loader
def loader_user(user_id):
	return models.Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
@login_required
def register():
    """Handles registering a new user.

    Returns:
        The template to be rended.
    """
    form = SignUpForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form.get("password") == request.form.get("confirmPassword"):
                    # Encrypt password
                    hashedPassword = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8') 
                    user = models.Users(username=request.form.get("username"), password=hashedPassword)
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
    """Handles login of a user.

    Returns:
        Redirects to the home page if login is successful.
    """
    form = LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = models.Users.query.filter_by(
                username=request.form.get("username")).first()
                if bcrypt.check_password_hash(user.password, request.form.get("password")):
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
@login_required
def logout():
    """Handles the logout of a user.

    Returns:
        Redirects to the home page.
    """
    logout_user()

    flash("Logged out successfully", "success")

    return redirect(url_for("home"))


@app.route("/manage-account")
@login_required
def manageAccount():
    """Displays tables contain all the users.

    Returns:
        The template to be rendered.
    """
    if current_user.username == "admin":
        users = db.session.query(models.Users).all()

        return render_template("manage_account.html", accounts=users)
    else:
        return redirect(url_for("home"))


@app.route("/delete-account/<account_id>", methods=["GET", "POST"])
@login_required
def deleteAccount(account_id):
    """Deletes a user.

    Args:
        account_id (int): id of the account to delete.

    Returns:
        Redirects back to the manage account page.
    """
    if current_user.username == "admin":
        try:
            user = db.session.query(models.Users).get(account_id)
            db.session.delete(user)
            db.session.commit()

            flash("Account has been deleted", "success")
        except (DataError, OperationalError, IntegrityError):
            flash("Account could not be deleted", "danger")
            
        users = db.session.query(models.Users).all()

    return render_template("manage_account.html", accounts=users)


@app.route("/edit-account/<account_id>", methods=["GET", "POST"])
@login_required
def editAccount(account_id):
    """Displays and allows the account details to be edited.

    Args:
        account_id (int): id of the account to edit.

    Returns:
        Redirects back to the manage account page if successful.
    """
    form = EditAccountForm()
    user = db.session.query(models.Users).get(account_id)
    
    if current_user.username == "admin":
        if form.validate_on_submit():
            try:
                if bcrypt.check_password_hash(user.password, request.form.get("currentPassword")):
                    if request.form.get("password") == request.form.get("confirmPassword"):
                        user.password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
                        user.username = request.form.get("username")
                        db.session.commit()
                        
                        flash("Account has been updated", "success")
                        
                        return redirect(url_for("manageAccount"))
                    else:
                        flash("New passwords does not match", "danger")
                else:
                    flash("Password does not match the old one", "danger")
            except IntegrityError:
                flash("This income name already exists", 'danger')
                
                return redirect(url_for("manageAccount"))
    
    # Empty the data fields in the from after it has been processed
    form.username.default = user.username
    form.process()
    
    return render_template("edit_account.html", account=user, form=form)


@app.route("/")
def home():
    """Renders the home page.

    Returns:
        The template to be rendered.
    """
    return render_template("index.html")
