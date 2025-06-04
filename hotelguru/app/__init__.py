from time import strptime
from datetime import datetime, timedelta
import requests
from apiflask import APIFlask
from flask import render_template, redirect, url_for, make_response, flash, request
from app.blueprints import verify_token
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.edit_user_form import editUserForm
from app.forms.booking_form import BookingForm
from app.forms.room_form import RoomForm
from config import Config
from app.extensions import db
from app.models import *
import calendar


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
        info = check_login()

        return render_template("index.html", info=info)


    def check_login():
        payload = verify_token(request.cookies.get("token"))
        info = {
            "logged_in": False,
            "name": "",
            "role": "",
        }

        if payload:
            info["logged_in"] = True
            info["name"] = payload["name"]
            info["role"] = payload["role"][0]

        return info

    @app.route("/register", methods=["GET", "POST"])
    def register():
        info = check_login()

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
                return render_template("register.html", form=form, info=info)

        return render_template("register.html", form=form, info=info)


    @app.route("/login", methods=["GET", "POST"])
    def login():
        info = check_login()

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
                return render_template("login.html", form=form, info=info)
            else:
                redir = make_response(redirect(url_for("index")))
                redir.set_cookie('token', response.json()["token"])
                return redir

        return render_template("login.html",  form=form, info=info)


    @app.route("/logout")
    def logout():
        redir = make_response(redirect(url_for("index")))
        redir.set_cookie("token", "", expires=0)
        flash("Successfully logged out")
        return redir


    @app.route("/room_list", methods=["GET"])
    def room_list():
        info = check_login()

        payload = verify_token(request.cookies.get("token"))

        role_name = ""

        if payload:
            role = payload["role"][0]
            role_name = role["name"]

        response = requests.get("http://localhost:8888/api/room/list_all")
        rooms = response.json()

        return render_template("room_list.html", rooms=rooms, info=info)


    @app.route("/edit_user", methods=["GET", "POST"])
    def edit_user():
        info = check_login()

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
                redir = make_response(redirect(url_for("index")))
                return redir
            else:
                flash("Something Went Wrong", category="error")
                render_template("edit_user.html", form=form, info=info)
        return render_template("edit_user.html", form=form, info=info)


    @app.route("/room/<int:id>", methods=["GET", "POST", "PUT"])
    def book_room(id):
        info = check_login()

        get_response = requests.get(f"http://localhost:8888/api/room/get/{id}")
        room = get_response.json()

        get_response = requests.get(f"http://localhost:8888/api/booking/list_all")
        bookings = get_response.json()

        bookings_list = []
        for booking in bookings:
            if booking["room_id"] == room["id"]:
                bookings_list.append(booking)

        token = request.cookies.get("token")
        payload = verify_token(token)
        user_id = payload["user_id"]


        if len(bookings_list) == 0:
            requests.put("http://localhost:8888/api/room/update_status",
                         json={
                             "id": room["id"],
                             "status": "Available"
                         },
                         headers={
                             "Authorization": f"Bearer {token}",
                             "Content-Type": "application/json"
                         })
        
        form = BookingForm()
        check_in = form.check_in.data
        check_out = form.check_out.data
        if form.comment.data is None:
            comment = ""
        else:
            comment = form.comment.data

        if form.validate_on_submit():
            error, error_msg = validate_booking(check_in, check_out, bookings_list)
            if error:
                flash(message=error_msg, category="error")
                redir = make_response(redirect(url_for("book_room", id=id)))
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
                    redir = make_response(redirect(url_for("book_room", id=id)))
                    return redir
                else:
                    flash("Something Went Wrong", category="error")

        return render_template("room_profile.html", room=room, id=room["id"], form=form, bookings_list=bookings_list, user_id=user_id, info=info)


    def validate_booking(check_in, check_out, bookings_list):
        error_msg = ""

        if check_out < check_in:
            error_msg = "Check out date must be later than check in date."
            return True, error_msg

        current_date = datetime.now().date()
        delta = check_in - current_date
        if delta.days < 3:
            error_msg = "Check in date must be 3 days from today."
            return True, error_msg

        intervals = []
        current_interval = [check_in + timedelta(days=x) for x in range((check_out - check_in).days + 1)]

        for booking in bookings_list:
            intervals.append([datetime.strptime(booking["check_in"], "%Y-%m-%d").date() + timedelta(days=x)
                              for x in range((datetime.strptime(booking["check_out"], "%Y-%m-%d").date() - datetime.strptime(booking["check_in"], "%Y-%m-%d").date()).days + 1)])

        for interval in intervals:
            if set(current_interval) & set(interval):
                error_msg = "Booking dates overlap with another booking."
                return True, error_msg

        return False, error_msg


    @app.route("/booking_list", methods=["GET"])
    def list_bookings():
        info = check_login()

        response = requests.get("http://localhost:8888/api/booking/list_all")
        bookings = response.json()

        return render_template("booking_list.html", bookings=bookings, info=info)


    @app.route("/check_in_guest/<int:id>", methods=["GET", "POST"])
    def check_in_guest(id):
        info = check_login()

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

        return render_template("booking_list.html", info=info)


    @app.route("/check_out_guest/<int:id>", methods=["GET", "POST"])
    def check_out_guest(id):
        info = check_login()

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

        return render_template("booking_list.html", info=info)


    @app.route("/delete_booking/<int:id>", methods=["GET", "DELETE"])
    def delete_booking(id):
        info = check_login()

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

        return render_template("booking_list.html", info=info)


    @app.route("/delete_room/<int:id>", methods=["GET", "DELETE"])
    def delete_room(id):
        info = check_login()

        token = request.cookies.get("token")

        get_response = requests.get(f"http://localhost:8888/api/booking/list_all")
        bookings = get_response.json()

        for booking in bookings:
            if booking["room_id"] == id:
                delete_booking(booking["id"])

        delete_response = requests.delete(f"http://localhost:8888/api/room/delete/{id}",
                                          headers={
                                              "Authorization": f"Bearer {token}",
                                              "Content-Type": "application/json"
                                          })

        if str(delete_response.status_code) == "200":
            flash("Room Successfully Deleted")
            redir = make_response(redirect(url_for("room_list")))
            return redir
        else:
            flash("Something Went Wrong", category="error")

        return render_template("/room_list.html", info=info)


    @app.route("/add_room", methods=["GET", "POST"])
    def add_room():
        info = check_login()

        token = request.cookies.get("token")
        form = RoomForm()

        type = form.type.data
        price = form.price.data
        capacity = form.capacity.data
        description = form.description.data

        if form.validate_on_submit():
            response = requests.post("http://localhost:8888/api/room/add",
                                     json={
                                         "type": type,
                                         "price": price,
                                         "capacity": capacity,
                                         "status": "Available",
                                         "description": description,
                                     },
                                     headers={
                                         "Authorization": f"Bearer {token}",
                                         "Content-Type": "application/json"
                                     })
            if str(response.status_code) == "201":
                flash("Room Successfully Added")
                return render_template("/add_room.html", form=form, info=info)
            else:
                flash("Something Went Wrong", category="error")

        return render_template("/add_room.html", form=form, info=info)


    @app.route("/edit_room/<int:id>", methods=["GET", "PUT", "POST"])
    def edit_room(id):
        info = check_login()

        token = request.cookies.get("token")
        form = RoomForm()

        type = form.type.data
        price = form.price.data
        capacity = form.capacity.data
        description = form.description.data

        if form.validate_on_submit():
            response = requests.put("http://localhost:8888/api/room/update",
                                     json={
                                         "id": id,
                                         "type": type,
                                         "price": price,
                                         "capacity": capacity,
                                         "description": description,
                                     },
                                     headers={
                                         "Authorization": f"Bearer {token}",
                                         "Content-Type": "application/json"
                                     })
            if str(response.status_code) == "200":
                flash("Room Successfully Edited")
                redir = make_response(redirect(url_for("room_list")))
                return redir
            else:
                flash("Something Went Wrong", category="error")

        return render_template("/edit_room.html", form=form, info=info)

    return app