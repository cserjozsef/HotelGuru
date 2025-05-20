from app.extensions import db
from app.blueprints.user.schemas import UserResponseSchema, RoleSchema
from app.models.user import User
from app.models.address import Address
from app.models.role import Role
from sqlalchemy import select
from app.auth import generate_token

class UserService:

    @staticmethod
    def user_registrate(request_data: dict):
        try:
            # Ellenőrzés, van-e már user ilyen emaillel
            existing_user = db.session.execute(select(User).filter_by(email=request_data["email"])).scalar_one_or_none()
            if existing_user:
                return False, "E-mail already exists!"

            # Címadat leválasztása a requestről
            address_data = request_data.pop("address")
            address = Address(**address_data)
            db.session.add(address)
            db.session.flush()  # hogy legyen ID-je az address-nek

            # User létrehozása a maradék adatokkal és az address objektummal
            user = User(**request_data, address=address)
            
            # Jelszó beállítása (nem a már eltávolított dict elemre hivatkozunk)
            user.set_password(request_data.get("password", ""))

            # Alapértelmezett szerepkör beállítása
            guest_role = db.session.execute(select(Role).filter_by(name="Guest")).scalar_one()
            user.roles.append(guest_role)

            db.session.add(user)
            db.session.commit()
            return True, UserResponseSchema().dump(user)
        except Exception as ex:
            return False, f"User registration failed: {ex}"

    @staticmethod
    def token_generate(user):
        roles = RoleSchema().dump(user.roles, many=True)
        return generate_token(user, roles)

    @staticmethod
    def user_login(request_data: dict):
        try:
            user = db.session.execute(select(User).filter_by(email=request_data["email"])).scalar_one()
            if not user.check_password(request_data["password"]):
                return False, "Incorrect e-mail or password!"

            user_schema = UserResponseSchema().dump(user)
            user_schema["token"] = UserService.token_generate(user)
            return True, user_schema
        except Exception:
            return False, "Incorrect login data!"
