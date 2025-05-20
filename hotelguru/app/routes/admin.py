from app.extensions import db
from app.models.room import Room
from flask import Blueprint



admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/rooms', methods=['GET'])
def list_all_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@admin_bp.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    data = request.get_json()
    room = Room.query.get_or_404(id)
    for key, value in data.items():
        setattr(room, key, value)
    db.session.commit()
    return jsonify(room.to_dict())

@admin_bp.route('/rooms/<int:id>/status', methods=['PUT'])
def change_room_status(id):
    data = request.get_json()
    room = Room.query.get_or_404(id)
    room.is_available = data['is_available']
    db.session.commit()
    return jsonify(room.to_dict())