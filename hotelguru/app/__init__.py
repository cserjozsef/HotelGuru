from time import strptime
from datetime import datetime
import requests
from apiflask import APIFlask
from flask import render_template, redirect, url_for, make_response, flash, request
from app.blueprints import verify_token
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.edit_user_form import editUserForm
from app.forms.booking_form import BookingForm
from config import Config
from app.extensions import db
from app.models import *


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
        payload = verify_token(request.cookies.get("token"))

        if payload:
            logged_in = True
            name = payload["name"]
            role = payload["role"][0]
            return render_template("index.html", name=name, role=role["name"], logged_in=logged_in)

        return render_template("index.html")


    @app.route("/register", methods=["GET", "POST"])
    def register():
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
            #verify_token(response.json()["token"])
            if str(response.status_code) != "200":
                flash("Invalid login credentials", category="error")
                return render_template("login.html", form=form)
            else:
                redir = make_response(redirect(url_for("index")))
                redir.set_cookie('token', response.json()["token"])
                return redir

        return render_template("login.html",  form=form)


    @app.route("/logout")
    def logout():
        redir = make_response(redirect(url_for("index")))
        redir.set_cookie("token", "", expires=0)
        flash("Successfully logged out")
        return redir


    @app.route("/room_list", methods=["GET"])
    def room_list():
        payload = verify_token(request.cookies.get("token"))

        logged_in = False
        if payload:
            logged_in = True

        response = requests.get("http://localhost:8888/api/room/list_all")
        rooms = response.json()

        return render_template("room_list.html", rooms=rooms, logged_in=logged_in)


    @app.route("/edit_user", methods=["GET", "POST"])
    def edit_user():
        form = editUserForm()
        token  = request.cookies.get("token")
        payload = verify_token(token)

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
                                         "id": payload["user_id"],
                                         "email": email,
                                         "password": password,
                                         "name": name,
                                         "phone": phone,
                                         "address": {
                                             "city": city,
                                             "postalcode": postalcode,
                                             "street": street
                                         }
                                     },
                                     headers={
                                         "Authorization": f"Bearer {token}",
                                         "Content-Type": "application/json"
                                     })
            if str(response.status_code) == "200":
                flash("Changes Saved")
                return render_template("edit_user.html", form=form)
            else:
                flash("Something Went Wrong", category="error")
        return render_template("edit_user.html", form=form)

    @app.route("/room/<int:id>", methods=["GET", "POST", "PUT"])
    def room_page(id):
        get_response = requests.get(f"http://localhost:8888/api/room/get/{id}")
        room = get_response.json()

        get_response = requests.get(f"http://localhost:8888/api/booking/list_all")
        bookings = get_response.json()

        check_in_date = ""
        check_out_date = ""
        bookings_list = []
        for booking in bookings:
            if booking["room_id"] == room["id"]:
                check_in_date = booking["check_in"]
                check_out_date = booking["check_out"]
                bookings_list.append(booking)

        token = request.cookies.get("token")
        payload = verify_token(token)
        user_id = payload["user_id"]
        
        form = BookingForm()
        check_in = form.check_in.data
        check_out = form.check_out.data
        if form.comment.data is None:
            comment = ""
        else:
            comment = form.comment.data

        if form.validate_on_submit():
            if validate_booking(check_in_date, check_out_date, check_in, check_out):
                flash("Already Booked on Selected Dates", category="error")
                redir = make_response(redirect(url_for("room_page", id=id)))
                return redir
            else:
                booking_response = requests.post("http://localhost:8888/api/booking/add",
                                       json={
                                           "check_out": check_out.strftime("%Y-%m-%d"),
                                           "check_in": check_in.strftime("%Y-%m-%d"),
                                           "comment": comment,
                                           "user_id": user_id,
                                           "room_id": room["id"],
                                           "invoice_id": 1
                                       },
                                       headers={
                                           "Authorization": f"Bearer {token}",
                                           "Content-Type": "application/json"
                                       })
                update_response = requests.put("http://localhost:8888/api/room/update_status",
                                                json={
                                                    "id": room["id"],
                                                    "status": "Booked"
                                                },
                                                headers={
                                                    "Authorization": f"Bearer {token}",
                                                    "Content-Type": "application/json"
                                                })

                if str(booking_response.status_code and update_response.status_code) == "200":
                    flash("Successfully Booked Room")
                    redir = make_response(redirect(url_for("room_list")))
                    return redir
                else:
                    flash("Something Went Wrong", category="error")

        return render_template("room_profile.html", room=room, id=room["id"], form=form, bookings_list=bookings_list)


    def validate_booking(check_in_db, check_out_db, check_in_input, check_out_input):
            present = datetime.now()
            if check_in_db=="":
                return False
            else:
                if ((check_in_input <= datetime.strptime(check_out_db, "%Y-%m-%d").date() and
                        check_out_input >= datetime.strptime(check_in_db, "%Y-%m-%d").date())
                        or present.date() > check_in_input):
                    return True
                else:
                    return False

    @app.route("/booking_list", methods=["GET"])
    def list_bookings():
        response = requests.get("http://localhost:8888/api/booking/list_all")
        bookings = response.json()

        return render_template("booking_list.html", bookings=bookings)

    @app.route("/check_in_guest/<int:id>", methods=["GET", "POST"])
    def check_in_guest(id):
        token = request.cookies.get("token")

        get_response = requests.get(f"http://localhost:8888/api/room/get/{id}")
        room = get_response.json()

        update_response = requests.put("http://localhost:8888/api/room/update_status",
                                       json={
                                           "id": room["id"],
                                           "status": "Occupied"
                                       },
                                       headers={
                                           "Authorization": f"Bearer {token}",
                                           "Content-Type": "application/json"
                                       })

        if str(update_response.status_code) == "200":
            flash("Guest Successfully Checked In")
            redir = make_response(redirect(url_for("list_bookings")))
            return redir
        else:
            flash("Something Went Wrong", category="error")

        return render_template("booking_list.html")


    @app.route("/check_out_guest/<int:id>", methods=["GET", "POST"])
    def check_out_guest(id):
        token = request.cookies.get("token")

        get_response = requests.get(f"http://localhost:8888/api/room/get/{id}")
        room = get_response.json()

        update_response = requests.put("http://localhost:8888/api/room/update_status",
                                       json={
                                           "id": room["id"],
                                           "status": "Available"
                                       },
                                       headers={
                                           "Authorization": f"Bearer {token}",
                                           "Content-Type": "application/json"
                                       })

        if str(update_response.status_code) == "200":
            flash("Guest Successfully Checked Out")
            redir = make_response(redirect(url_for("list_bookings")))
            return redir
        else:
            flash("Something Went Wrong", category="error")

        return render_template("booking_list.html")


    @app.route("/delete_booking/<int:id>", methods=["GET", "DELETE"])
    def delete_booking(id):
        token = request.cookies.get("token")
        
        delete_response = requests.delete(f"http://localhost:8888/api/booking/delete/{id}",
                                          headers={
                                           "Authorization": f"Bearer {token}",
                                           "Content-Type": "application/json"
                                       })

        if str(delete_response.status_code) == "200":
            flash("Booking Successfully Cancelled")
            redir = make_response(redirect(url_for("list_bookings")))
            return redir
        else:
            flash("Something Went Wrong", category="error")

        return render_template("booking_list.html")

    return app