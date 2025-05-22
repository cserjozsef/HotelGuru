from app.extensions import db
from app.blueprints.service.schemas import ServiceSchema
from app.models.service import Service
from sqlalchemy import select

class ServiceService:

    @staticmethod
    def service_list_all():
        service = db.session.execute(select(Service)).scalars()
        return True, ServiceSchema().dump(service, many=True)

    @staticmethod
    def service_add(request):
        try:
            service = Service(**request)
            db.session.add(service)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Service has been added"

    @staticmethod
    def service_update(request):
        try:
            service = db.session.get(Service, request["id"])
            if service:
                service.name = request["name"]
                service.price = request["price"]
                db.session.commit()
            else:
                return False, "Service does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, ServiceSchema().dump(service)

    @staticmethod
    def service_delete(id):
        try:
            service = db.session.get(Service, id)
            if not service:
                return False, "Service does not exist"
            elif service:
                db.session.delete(service)
                db.session.commit()
                return True, "Service has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def service_get(id):
        service = db.session.get(Service, id)
        if not service:
            return False, "Service does not exist"
        return True, ServiceSchema().dump(service)
