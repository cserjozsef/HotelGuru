from app.extensions import db
from app.blueprints.role.schemas import RoleResponseSchema, RoleSchema
from app.models.role import Role
from app.models.user import User
from sqlalchemy import select

class RoleService:

    @staticmethod
    def role_list_all():
        role = db.session.execute(select(Role)).scalars()
        return True, RoleSchema().dump(role, many=True)

    @staticmethod
    def role_add(request):
        try:
            role = Role(**request)
            db.session.add(role)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Role has been added"

    @staticmethod
    def role_update(request):
        try:
            role = db.session.get(Role, request["id"])
            if role:
                role.name = request["name"]
                db.session.commit()
            else:
                return False, "Role does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, RoleResponseSchema().dump(role)

    @staticmethod
    def role_delete(id):
        try:
            role = db.session.get(Role, id)
            if not role:
                return False, "Role does not exist"
            elif role:
                db.session.delete(role)
                db.session.commit()
                return True, "Role has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def role_get(id):
        role = db.session.get(Role, id)
        if not role:
            return False, "Role does not exist"
        return True, RoleResponseSchema().dump(role)

    @staticmethod
    def list_user_roles(id):
        user = db.session.get(User, id)
        if user is None:
            return False, "User not found"
        return True, RoleSchema().dump(obj=user.roles, many=True)