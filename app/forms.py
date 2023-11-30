from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

# Form to login


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    submit = SubmitField("Login")

# Form to sign up


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    confirmPassword = PasswordField("Confirm Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    submit = SubmitField("Sign Up")

# Form to edit account


class EditAccountForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    currentPassword = PasswordField("Current Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    confirmPassword = PasswordField("Confirm Password", validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    submit = SubmitField("Update")

# Form to add product


class AddProductForm(FlaskForm):
    productCode = StringField("Product Code", validators=[
        DataRequired(),
        Length(min=3, max=22)
    ])
    productName = StringField("Product Name", validators=[
        DataRequired(),
        Length(max=50)
    ])
    description = StringField("Description", validators=[
        DataRequired(),
        Length(max=200)
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(),
        NumberRange(min=0.01, max=1000000)
    ])
    submit = SubmitField("Add")

# Form to add product


class EditProductForm(FlaskForm):
    productCode = StringField("Product Code", validators=[
        DataRequired(),
        Length(min=3, max=22)
    ])
    productName = StringField("Product Name", validators=[
        DataRequired(),
        Length(max=50)
    ])
    description = StringField("Description", validators=[
        DataRequired(),
        Length(max=200)
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(),
        NumberRange(min=0.01, max=1000000)
    ])
    submit = SubmitField("Edit")
