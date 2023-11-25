from app import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    """Stores the user's details.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Product(db.Model):
    """Product table to store product details.
    """
    id = db.Column(db.Integer, primary_key=True)
    productCode = db.Column(db.String(250), unique=True, nullable=False)
    productName = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rate = db.Column(db.Float, nullable=False)

class StockIn(db.Model):
    """StockIn table to store stock in.
    """
    id = db.Column(db.Integer, primary_key=True)
    batchCode = db.Column(db.Integer, unique=True, nullable=False)
    batchDate = db.Column(db.Date, nullable=False)

class StockInDetail(db.Model):
    """StockInDetail table to store stock in details.
    """
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey("Product.id"))
    stockInId = db.Column(db.Integer, db.ForeignKey("StockIn.id"))
    quantity = db.Column(db.Integer, nullable=False)