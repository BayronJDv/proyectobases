from flask import render_template,  flash, redirect, url_for
from app.auth.forms import *
from app.auth import authentication
from app.auth.models import User,Client,Userm
from flask_login import login_user, logout_user, login_required, current_user


@authentication.route("/register", methods=["GET","POST"])
def register_user():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data,
            address=form.address.data,
            clientid=form.clientid.data
        )
        flash("Registration Done...")
        return redirect(url_for("authentication.log_in_user"))
    return render_template("registration.html", form=form)

@authentication.route("/registerClient", methods=["GET","POST"])
def register_client():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    form = RegistrationclientForm()
    if form.validate_on_submit():
        Client.create_client(
            name = form.name.data,
            address = form.address.data,
            email= form.email.data,
            telephone= form.telephone.data
        )
        flash("Registration Done... Now you can create a user with yout client id ")
        return redirect(url_for("authentication.register_user")) 
    return render_template("rclient.html", form=form)
@authentication.route("/")
def index():
    return render_template("index.html")

@authentication.route("/login", methods=["GET","POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("You are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, form.stay_loggedin.data)
            print(user.user_name)
            return redirect(url_for("authentication.homepage"))
        
        men = Userm.query.filter_by(userm_email=form.email.data).first()
        if men and men.checkm_password(form.password.data):
            login_user(men, form.stay_loggedin.data)
            print("Esta entrando a loginMens")
            return redirect(url_for("authentication.homepagem"))

        flash("Invalid credentials...")
        return redirect(url_for("authentication.log_in_user"))
    
    return render_template("login.html", form=form)


@authentication.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html")

@authentication.route("/homepagem")
@login_required
def homepagem():
    return render_template("homepagem.html")


@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():      
    logout_user()
    return redirect(url_for("authentication.log_in_user"))

@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@authentication.route("/pruebas")
def pruebas():
    return render_template('pruebas.html')
