from app.extensions import db
from app.blueprints.amenity.schemas import AmenitySchema, AmenityUpdateSchema
from app.models.amenity import Amenity
from sqlalchemy import select


class AmenityService:

    @staticmethod
    def amenity_list_all():
        amenity = db.session.execute(select(Amenity)).scalars()
        return True, AmenitySchema().dump(amenity, many=True)

    @staticmethod
    def amenity_add(request):
        try:
            amenity = Amenity(**request)
            db.session.add(amenity)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Amenity has been added"

    @staticmethod
    def amenity_update(request):
        try:
            amenity = db.session.get(Amenity, request["id"])
            if amenity:
                amenity.name = request["name"]
                db.session.commit()
            else:
                return False, "Amenity does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, AmenitySchema().dump(amenity)

    @staticmethod
    def amenity_delete(id):
        try:
            amenity = db.session.get(Amenity, id)
            if not amenity:
                return False, "Amenity does not exist"
            elif amenity:
                db.session.delete(amenity)
                db.session.commit()
                return True, "Amenity has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def amenity_get(id):
        amenity = db.session.get(Amenity, id)
        if not amenity:
            return False, "Amenity does not exist"
        return True, AmenitySchema().dump(amenity)
