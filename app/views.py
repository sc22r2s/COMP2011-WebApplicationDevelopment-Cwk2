from flask import render_template
# , flash, redirect, request
from app import app, db, admin, models
from flask_admin.contrib.sqla import ModelView
# from sqlalchemy.exc import IntegrityError, DataError, OperationalError
# from sqlalchemy.sql import functions
# from .forms import ()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
