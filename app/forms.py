from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, FloatField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

# Form to login 
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    submit = SubmitField('Login')

# Form to sign up
class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    confirmPassword = PasswordField('Confirm Password', validators=[
    DataRequired(),
    Length(min=4, max=21)
    ])
    submit = SubmitField('Sign Up')

# Form to edit account
class EditAccountForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=21)
    ])
    currentPassword = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=21)
    ])
    password = PasswordField('Confirm Password', validators=[
    DataRequired(),
    Length(min=4, max=21)
    ])
    confirmPassword = PasswordField('Confirm Password', validators=[
    DataRequired(),
    Length(min=4, max=21)
    ])
    submit = SubmitField('Update')