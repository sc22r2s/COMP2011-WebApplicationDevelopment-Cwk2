from flask import render_template, request, redirect, url_for
from app import app, db, admin, models, login_manager
from flask_login import UserMixin, login_user, logout_user


@login_manager.user_loader
def loader_user(user_id):
	return models.Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = models.Users(username=request.form.get("username"),
					password=request.form.get("password"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = models.Users.query.filter_by(
			username=request.form.get("username")).first()
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))


@app.route("/")
def home():
	return render_template("index.html")
