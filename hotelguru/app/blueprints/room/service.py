from app.extensions import db
from app.blueprints.room.schemas import RoomSchema, RoomUpdateSchema
from app.models.room import Room
from sqlalchemy import select

class RoomService:

    @staticmethod
    def room_list_all():
        room = db.session.execute(select(Room)).scalars()
        return True, RoomSchema().dump(room, many=True)

    @staticmethod
    def room_add(request):
        try:
            room = Room(**request)
            db.session.add(room)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Room has been added"

    @staticmethod
    def room_update(request):
        try:
            room = db.session.get(Room, request["id"])
            if room:
                room.type = request["type"]
                room.price = request["price"]
                room.capacity = request["capacity"]
                room.status = request["status"]
                room.description = request["description"]
                db.session.commit()
            else:
                return False, "Room does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, RoomSchema().dump(room)

    @staticmethod
    def room_delete(id):
        try:
            room = db.session.get(Room, id)
            if not room:
                return False, "Room does not exist"
            elif room:
                db.session.delete(room)
                db.session.commit()
                return True, "Room has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def room_get(id):
        room = db.session.get(Room, id)
        if not room:
            return False, "Room does not exist"
        return True, RoomSchema().dump(room)
