from flask import Blueprint, request, jsonify
from models import db, User, Room, Booking, Service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/rooms/available', methods=['GET'])
def list_available_rooms():
    rooms = Room.query.filter_by(is_available=True).all()
    return jsonify([room.to_dict() for room in rooms])

@user_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    booking = Booking(**data)
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201

@user_bp.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return '', 204

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    user = User.query.get(data['id'])
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/services', methods=['POST'])
def order_service():
    data = request.get_json()
    service = Service(**data)
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201