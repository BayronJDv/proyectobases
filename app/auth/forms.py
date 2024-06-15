
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User

#used to verify 
def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError("Email already exists. !!!!")

# used to register a user
class RegistrationForm(FlaskForm):
    choices = [('client', 'client'),
               ('delivery', 'delivery')]
    name = StringField("Name", validators=[DataRequired(), Length(4,16, message="Between 4 to 16 characters")])
    email = StringField("E-mail", validators=[DataRequired(), Email(), email_exists])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="Password must match!!!")])
    address = StringField("Address", validators=[DataRequired()])
    clientid = StringField("Client ID/Delivery ID", validators=[DataRequired()])
    confirm = PasswordField("Confirm", validators=[DataRequired()])
    type = SelectField("register as", choices = choices, validators=[DataRequired()])
    submit = SubmitField("Register")

# used to log in 
class LoginForm(FlaskForm):
    email= StringField("E-mail", validators=[DataRequired(), Email()])
    password= PasswordField("Password", validators=[DataRequired()])
    stay_loggedin= BooleanField("Remember Me!")
    submit= SubmitField("Login")

#used to register a client
class RegistrationclientForm(FlaskForm):
    name= StringField("Name", validators=[DataRequired()])
    address= StringField("address", validators=[DataRequired()])
    email= StringField("E-mail", validators=[DataRequired(), Email(), email_exists])
    telephone= StringField("telephone", validators=[DataRequired()])

# used to register a delivery
class RegistrationDeliveryForm(FlaskForm):
    name= StringField("Name", validators=[DataRequired()])
    address= StringField("address", validators=[DataRequired()])
    email= StringField("E-mail", validators=[DataRequired(), Email(), email_exists])
    telephone= StringField("telephone", validators=[DataRequired()])