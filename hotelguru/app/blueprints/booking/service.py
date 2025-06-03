from app.extensions import db
from app.blueprints.booking.schemas import BookingSchema, BookingUpdateSchema, BookingRequestSchema
from app.models.booking import Booking
from datetime import datetime
from sqlalchemy import select

class BookingService:

    @staticmethod
    def booking_list_all():
        booking = db.session.execute(select(Booking)).scalars()
        return True, BookingSchema().dump(booking, many=True)

    @staticmethod
    def booking_add(request):
        try:
            booking = Booking(**request)
            db.session.add(booking)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Booking has been added"

    @staticmethod
    def booking_update(request):
        try:
            booking = db.session.get(Booking, request["id"])
            if booking:
                booking.check_in = datetime.strptime(request["check_in"], '%Y-%m-%d')
                booking.check_out = datetime.strptime(request["check_out"], '%Y-%m-%d')
                booking.comment = request["comment"]
                db.session.commit()
            else:
                return False, "Booking does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, BookingUpdateSchema().dump(booking)

    @staticmethod
    def booking_delete(id):
        try:
            booking = db.session.get(Booking, id)
            if not booking:
                return False, "Booking does not exist"
            elif booking:
                db.session.delete(booking)
                db.session.commit()
                return True, "Booking has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def booking_get(id):
        booking = db.session.get(Booking, id)
        if not booking:
            return False, "Booking does not exist"
        return True, BookingSchema().dump(booking)
