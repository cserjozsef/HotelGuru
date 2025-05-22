from app.extensions import db
from app.blueprints.address.schemas import AddressSchema
from app.models.address import Address
from sqlalchemy import select

class AddressService:

    @staticmethod
    def address_list_all():
        address = db.session.execute(select(Address)).scalars()
        return True, AddressSchema().dump(address, many=True)

    @staticmethod
    def address_add(request):
        try:
            address = Address(**request)
            db.session.add(address)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Address has been added"

    @staticmethod
    def address_update(request):
        try:
            address = db.session.get(Address, request["id"])
            if address:
                address.city = request["city"]
                address.street = request["street"]
                address.postalcode = request["postalcode"]
                db.session.commit()
            else:
                return False, "Address does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, AddressSchema().dump(address)

    @staticmethod
    def address_delete(id):
        try:
            address = db.session.get(Address, id)
            if not address:
                return False, "Address does not exist"
            elif address:
                db.session.delete(address)
                db.session.commit()
                return True, "Address has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def address_get(id):
        address = db.session.get(Address, id)
        if not address:
            return False, "Address does not exist"
        return True, AddressSchema().dump(address)
