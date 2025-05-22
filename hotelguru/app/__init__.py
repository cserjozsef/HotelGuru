import requests
from apiflask import APIFlask
from flask import render_template, redirect, url_for, make_response, flash
from app.blueprints import verify_token
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
#from app.forms.edit_user_form import editUserForm
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors=True,
                   title="Hotelguru API",
                   docs_path="/swagger")

    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix="/api")


    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def registrate():
        form = RegisterForm()

        email = form.email.data
        password = form.password.data
        name = form.name.data
        phone = form.phone.data
        city = form.city.data
        postalcode = form.postalcode.data
        street = form.street.data

        if form.validate_on_submit():
            response = requests.post("http://localhost:8888/api/user/register",
            json={
                "email": email,
                "password": password,
                "name": name,
                "phone": phone,
                "address": {
                    "city": city,
                    "postalcode": postalcode,
                    "street": street
                }
            })

            if str(response.status_code) == "200":
                flash("Successful registration")
                redir = make_response(redirect(url_for("index")))
                return redir
            else:
                flash("Email already in use", category="error")
                return render_template("register.html", form=form)

        return render_template("register.html", form=form)


    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()

        email = form.email.data
        password = form.password.data

        if form.validate_on_submit():
            response = requests.post("http://localhost:8888/api/user/login",
            json={
                "email": email,
                "password": password
            })
            if verify_token(response.json()["token"]):
                redir = make_response(redirect(url_for("index")))
                return redir
            else:
                flash("Invalid login credentials", category="error")
                return render_template("login.html", form=form)

        return render_template("login.html",  form=form)

    @app.route("/room_list", methods=["GET"])
    def room_list():
        response = requests.get("http://localhost:8888/api/room/list_all")
        rooms = response.json()
        return render_template("room_list.html", rooms=rooms)


    '''@app.route("/edit_user", methods=["GET", "POST"])
    def edit_user():
        form = editUserForm()

        email = form.email.data
        password = form.password.data
        name = form.name.data
        phone = form.phone.data
        city = form.city.data
        postalcode = form.postalcode.data
        street = form.street.data

        if form.validate_on_submit():
            response = requests.post("http://localhost:8888/api/user/update",
                                     json={
                                         "email": email,
                                         "password": password,
                                         "name": name,
                                         "phone": phone,
                                         "address": {
                                             "city": city,
                                             "postalcode": postalcode,
                                             "street": street
                                         }
                                     })
            if verify_token(response.json()["token"]):
                return render_template("edit_user.html", form=form)
            else:
                flash("Log In First", category="error")
                return render_template("index.html")
        return render_template("index.html")'''


    return app