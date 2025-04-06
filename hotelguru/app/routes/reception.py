from flask import Blueprint, jsonify
from models import db, Booking, Invoice

reception_bp = Blueprint('reception_bp', __name__)

@reception_bp.route('/bookings/<int:id>/confirm', methods=['PUT'])
def confirm_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.is_confirmed = True
    db.session.commit()
    return jsonify(booking.to_dict())

@reception_bp.route('/checkin/<int:id>', methods=['PUT'])
def check_in(id):
    booking = Booking.query.get_or_404(id)
    booking.checked_in = True
    db.session.commit()
    return jsonify(booking.to_dict())

@reception_bp.route('/invoice/<int:id>', methods=['GET'])
def get_invoice(id):
    invoice = Invoice.query.filter_by(booking_id=id).first_or_404()
    return jsonify(invoice.to_dict())