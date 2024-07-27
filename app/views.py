from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db, admin, models, login_manager, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.sql import text
from sqlalchemy.exc import (IntegrityError, DataError, OperationalError,
                            PendingRollbackError)
from sqlalchemy.orm.exc import UnmappedInstanceError
from .forms import (LoginForm, SignUpForm, EditAccountForm,
                    AddProductForm, EditProductForm)

import json
import datetime
import sqlite3


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
                if (request.form.get("password") ==
                        request.form.get("confirmPassword")):
                    # Encrypt password
                    hashedPassword = bcrypt.generate_password_hash(
                        request.form.get("password")).decode('utf-8')
                    user = models.Users(username=request.form.get(
                        "username"), password=hashedPassword)
                    db.session.add(user)
                    db.session.commit()

                    flash("User created successfully", "success")

                    return redirect(url_for("login"))
                else:  # Passwords does not match
                    flash("Passwords does not match", "danger")
            # Username already exists
            except (IntegrityError, PendingRollbackError):
                db.session.rollback()
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
                if bcrypt.check_password_hash(user.password,
                                              request.form.get("password")):
                    login_user(user)

                    flash("Logged in successfully", "success")

                    return redirect(url_for("home"))
                else:
                    # Clear form fields
                    form = LoginForm(formdata=None)
                    form.process()

                    flash("Incorrect username or password", "danger")
            except (IntegrityError, AttributeError):
                # Clear form fields
                form = LoginForm(formdata=None)
                form.process()

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
    """Displays a table containing all the users.

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
    try:
        user = db.session.query(models.Users).get(account_id)

        if current_user.username == "admin":
            if form.validate_on_submit():
                try:
                    if bcrypt.check_password_hash(
                            user.password,
                            request.form.get("currentPassword")):
                        if (request.form.get("password") ==
                                request.form.get("confirmPassword")):
                            user.password = bcrypt.generate_password_hash(
                                request.form.get("password")).decode('utf-8')
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

            # Insert data in the form
            form.username.default = user.username
            form.process()

            return render_template("edit_account.html", account=user,
                                   form=form)

    except (IntegrityError, AttributeError):
        flash("This account does not exist", "danger")

        return redirect(url_for("home"))


@app.route("/add-product", methods=["GET", "POST"])
@login_required
def addProduct():
    """Handles adding a product.

    Returns:
        The template to be rendered.
    """
    form = AddProductForm()

    if current_user.username == "admin":
        if form.validate_on_submit():
            try:
                product = models.Product(
                    productCode=request.form.get("productCode"),
                    productName=request.form.get(
                        "productName"),
                    description=request.form.get(
                        "description"),
                    rate=request.form.get("rate"))
                db.session.add(product)
                db.session.commit()

                flash("Product has been added successfully", "success")

                # Clear form fields
                form = AddProductForm(formdata=None)
                form.process()

                return render_template("add_product.html", form=form)

            except (IntegrityError, AttributeError, PendingRollbackError):
                db.session.rollback()

                flash("Product can't have the same name", "danger")

                return render_template("add_product.html", form=form)

        # Clear form fields
        form = AddProductForm(formdata=None)
        form.process()

        return render_template("add_product.html", form=form)

    return redirect(url_for("home"))


@app.route("/view-product", methods=["GET", "POST"])
@login_required
def viewProduct():
    """Displays a table containing all the products.

    Returns:
        The template to be rendered.
    """
    products = db.session.query(models.Product).all()

    if current_user.username == "admin":

        return render_template("view_product.html", products=products,
                               admin=True)
    else:
        return render_template("view_product.html", products=products,
                               admin=False)


@app.route("/delete-product/<product_id>", methods=["GET", "POST"])
@login_required
def deleteProduct(product_id):
    """Deletes a product.

    Args:
        product_id (int): id of the product to delete.

    Returns:
        Redirects back to the view product page.
    """
    if current_user.username == "admin":
        try:
            product = db.session.query(models.Product).get(product_id)
            db.session.execute('pragma foreign_keys=on')
            db.session.delete(product)
            db.session.commit()

            flash("Product has been deleted", "success")

            products = db.session.query(models.Product).all()
            return render_template("view_product.html", products=products,
                                   admin=True)

        except (IntegrityError, AttributeError, PendingRollbackError,
                UnmappedInstanceError):
            flash("This product is already added in stock or it does not "
                  "exist", "danger")

            return redirect(url_for("viewProduct"))


@app.route("/edit-product/<product_id>", methods=["GET", "POST"])
@login_required
def editProduct(product_id):
    """Displays and allows the product details to be edited.

    Args:
        product_id (int): id of the product to edit.

    Returns:
        Redirects back to the view product page if successful.
    """
    form = EditProductForm()
    try:
        product = db.session.query(models.Product).get(product_id)

        if form.validate_on_submit():
            try:
                product.productCode = request.form.get("productCode")
                product.productName = request.form.get("productName")
                product.description = request.form.get("description")
                product.rate = request.form.get("rate")

                db.session.commit()

                flash("Product has been successfully updated", "success")

                return redirect(url_for("viewProduct"))

            except (IntegrityError, AttributeError, PendingRollbackError):
                db.session.rollback()

                flash("Product could not be updated", "danger")

                return redirect("/edit-product/" + product_id)

        # Insert data in the form
        form.productCode.default = product.productCode
        form.productName.default = product.productName
        form.description.default = product.description
        form.rate.default = product.rate
        form.process()

        return render_template("edit_product.html", form=form, product=product)

    except (IntegrityError, AttributeError, PendingRollbackError):
        flash("Product could not be updated", "danger")

        return redirect(url_for("viewProduct"))


@app.route("/stock", methods=["GET", "POST"])
@login_required
def stock():
    """Displays and allows stocks to be added.

    Returns:
        The template to be rendered.
    """
    return render_template("stock.html")


@app.route("/ajax/display-product-detail", methods=["GET", "POST"])
def displayProductDetail():
    code = request.args.get("productCode")

    try:
        product = models.Product.query.filter_by(productCode=code).first()

        return jsonify({"id": product.id,
                        "productCode": product.productCode,
                        "productName": product.productName,
                        "description": product.description,
                        "rate": product.rate})

    except AttributeError:
        return jsonify({"error": "This product does not exist"})


@app.route("/ajax/add-batch", methods=["GET", "POST"])
def addBatch():
    """Adds a batch to the database.

    Returns:
        json: success or error message.
    """
    batch = json.loads(request.args.get("batch"))

    try:
        batch_ = models.StockInOut(batchCode=batch["batchCode"],
                                   batchDate=datetime.date.today(),
                                   inOut=batch["batchDirection"])
        db.session.add(batch_)
        db.session.commit()

        for items in batch["productDetail"]:
            stockInOut = models.StockInOutDetail(productId=items["productId"],
                                                 stockInOutId=batch_.id,
                                                 quantity=items["quantity"])
            db.session.add(stockInOut)

        db.session.commit()

        # flash("Batch added successfully", "success")
        # return render_template("stock_in.html")
        return jsonify({"success": "Batch added successfully"})

    except (IntegrityError, AttributeError, PendingRollbackError):
        db.session.rollback()
        # flash("An error occurred", "danger")

        # return render_template("stock_in.html")
        # return {"error": "An error occurred"}

        return jsonify({"error": ""})


@app.route("/view-batch")
def viewBatch():
    """Displayed the batches added.

    Returns:
        The template to be rendered.
    """
    query = ("SELECT id, batchCode, batchDate, CASE inOut WHEN 0 THEN \"Batch "
             "In\" ELSE \"Batch Out\" END AS batchDirection FROM "
             "stock_in_out")
    
    try:
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()

        batches = cursor.execute(query).fetchall()

        cursor.close()
        connection.close()

        return render_template("view_batch.html", batches=batches)

    except sqlite3.Error:
        flash("Error occurred", "danger")

    return render_template("view_batch.html")


@app.route("/view-batch-detail/<batch_id>")
def viewBatchDetail(batch_id):
    """Displays the details of a specific batch.

    Args:
        batch_id (int): The id of the batch.

    Returns:
        The template to be rendered.
    """
    query = ("SELECT batchCode, CASE inOut WHEN 0 THEN \"Batch In\" ELSE \"Batch Out\" END, batchDate, productCode, productName, quantity "
             "FROM stock_in_out_detail AS siod, product AS p, stock_in_out as sio "
             "WHERE siod.productId = p.id AND sio.id = stockInOutId "
             "AND stockInOutId = " + batch_id)
    
    try:
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()

        details = cursor.execute(query).fetchall()

        cursor.close()
        connection.close()

        return render_template("view_batch_detail.html", details=details)

    except sqlite3.Error:
        flash("Error occurred", "danger")

    return render_template("view_batch_detail.html")


@app.route("/view-stock")
def viewStock():
    """Displays the stocks that has been added.

    Returns:
        The template to be rendered.
    """
    query = ("SELECT productId, productCode, productName, sum(case inOut when "
             "0 then quantity else -quantity end) as stockBalance FROM "
             "stock_in_out as sio, stock_in_out_detail as siod, product as p "
             "WHERE sio.id = siod.stockInOutId and p.id = siod.productId GROUP"
             " BY productId, productCode, productName")

    try:
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()

        stocks = cursor.execute(query).fetchall()

        cursor.close()
        connection.close()

        return render_template("view_stock.html", stocks=stocks)

    except sqlite3.Error:
        flash("Error occurred", "danger")

    return render_template("view_stock.html", stocks=stocks)


@app.route("/view-stock-detail/<product_id>", methods=["GET", "POST"])
def viewStockDetail(product_id):
    """Displays the details of a particular product.

    Args:
        product_id (int): Id of the product.

    Returns:
        The template to be rendered.
    """
    query = ("SELECT productCode, productName, batchCode, batchDate,"
             " case inOut when 0 then quantity else -quantity end as"
             " stockBalance FROM stock_in_out as sio, "
             "stock_in_out_detail as siod, product as p WHERE "
             "siod.productId = " + product_id + " and sio.id = "
             "siod.stockInOutId and p.id = siod.productId")

    try:
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()

        details = cursor.execute(query).fetchall()

        cursor.close()
        connection.close()

        return render_template("view_stock_detail.html", details=details)

    except sqlite3.Error:
        flash("Error occurred", "danger")

    return render_template("view_stock_detail.html")


@app.route("/")
def home():
    """Renders the home page.

    Returns:
        The template to be rendered.
    """
    db.session.execute(text('pragma foreign_keys=on'))

    return render_template("index.html")
