from flask import Blueprint, jsonify, request, g
from apiflask import APIBlueprint
from app.extensions import db
from app.models.invoice import Invoice
from app.models.user import User
from app.models.room import Room, StatusEnum
from app.models.booking import Booking
from app.models.service import Service
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema
from config import Config

from app.auth import generate_token, auth  # JWT token generálás és autentikáció

user_bp = APIBlueprint('user', __name__, tag="User")

def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors=True, title="HotelGuru API", docs_path="/swagger")
    app.config.from_object(config_class)

    app.register_blueprint(user_bp, url_prefix='/api/user')

    return app

def room_to_dict(room):
    return {
        "id": room.id,
        "type": room.type,
        "price": room.price,
        "capacity": room.capacity,
        "status": room.status.name if isinstance(room.status, StatusEnum) else room.status,
        "description": room.description,
        "amenities": room.amenities
    }

def booking_to_dict(booking):
    return {
        "id": booking.id,
        "check_in": booking.check_in.isoformat() if booking.check_in else None,
        "check_out": booking.check_out.isoformat() if booking.check_out else None,
        "days": booking.days,
        "comment": booking.comment,
        "user_id": booking.user_id,
        "invoice_id": booking.invoice_id
    }

def user_to_dict(user):
    return {
        "id": user.id,
        "name": getattr(user, "fname", None) or getattr(user, "name", None),
        "email": user.email,
        "phone": user.phone
    }

def service_to_dict(service):
    return {
        "id": service.id,
        "booking_id": service.booking_id,
        "invoice_id": service.invoice_id,
        "name": service.name,
        "price": service.price
    }

@user_bp.route('/rooms/available', methods=['GET'])
def list_available_rooms():
    rooms = Room.query.filter_by(status=StatusEnum.Available).all()
    return jsonify([room_to_dict(room) for room in rooms])

# JWT-vel védett végpont, user_id a tokenből jön
@user_bp.route('/bookings', methods=['POST'])
@auth.login_required
def create_booking():
    data = request.get_json()
    user_id = g.current_user_id
    booking = Booking(**data, user_id=user_id)
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking_to_dict(booking)), 201

@user_bp.route('/bookings/<int:id>', methods=['DELETE'])
@auth.login_required
def cancel_booking(id):
    user_id = g.current_user_id
    booking = Booking.query.get_or_404(id)
    if booking.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(booking)
    db.session.commit()
    return '', 204

@user_bp.route('/profile', methods=['PUT'])
@auth.login_required
def update_profile():
    data = request.get_json()
    user_id = g.current_user_id
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.fname = data.get('name', user.fname)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    db.session.commit()
    return jsonify(user_to_dict(user))

@user_bp.route('/services', methods=['POST'])
@auth.login_required
def order_service():
    data = request.get_json()
    user_id = g.current_user_id
    service = Service(**data)
    db.session.add(service)
    db.session.commit()
    return jsonify(service_to_dict(service)), 201

@user_bp.post('/registrate')
@user_bp.input(UserRequestSchema, location="json")
@user_bp.output(UserResponseSchema)
def user_registrate(json_data):
    try:
        existing_user = db.session.execute(select(User).filter_by(email=json_data["email"])).scalar_one_or_none()
        if existing_user:
            return {"message": "E-mail already exists!"}, 400

        address_data = json_data.pop("address")
        address = Address(**address_data)
        db.session.add(address)
        db.session.flush()

        user = User(**json_data, address=address)
        user.set_password(json_data["password"])

        guest_role = db.session.execute(select(Role).filter_by(name="Guest")).scalar_one()
        user.roles.append(guest_role)

        db.session.add(user)
        db.session.commit()

        return UserResponseSchema().dump(user)

    except Exception as ex:
        return {"message": f"User registration failed: {ex}"}, 500

# Új endpoint: login, token generálással
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials.'}), 401
