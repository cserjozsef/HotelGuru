from app.extensions import db
from app.blueprints.user.schemas import UserResponseSchema, RoleSchema, PayloadSchema, UserSchema
from app.models.user import User
from app.models.address import Address
from app.models.role import Role
from datetime import datetime, timedelta
from authlib.jose import jwt
from flask import current_app
from sqlalchemy import select

class UserService:
    
    @staticmethod
    def user_register(request):
        try:
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "E-mail already exists!"
            request["address"] = Address(**request["address"])
            user = User(**request)
            user.set_password(user.password)
            user.roles.append(db.session.get(Role, 2))
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            return False, "Incorrect User data!"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(User).filter_by(email=request["email"])).scalar_one()
            user_schema = UserResponseSchema().dump(user)
            user_schema["token"] = UserService.token_generate(user)
            if not user.check_password(request["password"]):
                return False, "Incorrect email or password!"
        except Exception as ex:
            return False, "Incorrect Login data!"
        return True, user_schema

    @staticmethod
    def user_update(request):
        try:
            user = db.session.get(User, request["id"])
            address = db.session.get(Address, user.address_id)
            if user:
                user.email = request["email"]
                user.name = request["name"]
                user.set_password(request["password"])
                address.city = request["address"].get("city")
                address.street = request["address"].get("street")
                address.postalcode = request["address"].get("postalcode")
                user.address = address
                user.phone = request["phone"]
                db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_delete(id):
        try:
            user = db.session.get(User, id)
            address = db.session.get(Address, user.address_id)
            if not user:
                return False, "User does not exist"
            elif user:
                db.session.delete(user)
                db.session.delete(address)
                db.session.commit()
                return True, f"User \"{user.name}\" has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True

    @staticmethod
    def user_get(id):
        user = db.session.get(User, id)
        if not user:
            return False, "User does not exist"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_list_all():
        user = db.session.execute(select(User)).scalars()
        return True, UserSchema().dump(user, many=True)


    @staticmethod
    def token_generate(user: User):
        payload = PayloadSchema()
        payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
        payload.user_id = user.id
        payload.email = user.email
        payload.name = user.name
        payload.role = RoleSchema().dump(obj=user.roles, many=True)

        return jwt.encode({'alg': 'RS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()