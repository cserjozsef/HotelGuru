from __future__ import annotations
from app import db
from app import create_app
from app.models.amenity import Amenity
from config import Config
from datetime import datetime
from app.models.booking import Booking
from app.models.user import User
from app.models.role import Role
from app.models.room import Room
from app.models.invoice import Invoice
from app.models.service import Service
from app.models.address import Address


app = create_app(config_class=Config)
app.app_context().push()


db.drop_all()
db.create_all()

#Roles
db.session.add_all([ Role(name="Administrator"),
                     Role(name="User"),
                     Role(name="Receptionist")])

#Services
db.session.add_all([ Service(name="Massage", price=10000),
                     Service(name="Sauna", price=20000),
                     Service(name="Room Service", price=30000),
                     Service(name="Golf", price=40000)])

#Amenities
db.session.add_all([ Amenity(name="Air conditioning"),
                     Amenity(name="Nice view"),
                     Amenity(name="Private pool"),
                     Amenity(name="Balcony")])

#Address
db.session.add(Address(city = "teszt",  street = "teszt utca", postalcode=1111))

#Users
user = User( email="user@gmail.com", name="User", phone="06121231234")
admin = User( email="admin@gmail.com", name="Admin", phone="06121231234")
rec = User( email="rec@gmail.com", name="Receptionist", phone="06121231234")
test = User( email="teszt@teszt.com", name="Teszt", phone="kitérdekel")

user.address = db.session.get(Address, 1)
user.set_password("asd")

admin.address = db.session.get(Address, 1)
admin.set_password("asd")

rec.address = db.session.get(Address, 1)
rec.set_password("asd")

test.address = db.session.get(Address, 1)
test.set_password("test")

db.session.add(user)
db.session.add(admin)
db.session.add(rec)
db.session.add(test)

u = db.session.get(User, 1)
u.roles.append(db.session.get(Role, 2))

a = db.session.get(User, 2)
a.roles.append(db.session.get(Role, 1))

r = db.session.get(User, 3)
r.roles.append(db.session.get(Role, 3))

t = db.session.get(User, 4)
t.roles.append(db.session.get(Role, 1))
t.roles.append(db.session.get(Role, 2))
t.roles.append(db.session.get(Role, 3))

#Room
db.session.add(Room(type="single", price=30000, capacity=2, status="Available", description="Single room etc etc"))
r = db.session.get(Room, 1)
r.amenities.append(db.session.get(Amenity, 1))
db.session.add(Room(type="deluxe", price=150000, capacity=5, status="Available", description="description"))
r = db.session.get(Room, 2)
r.amenities.append(db.session.get(Amenity, 1))
r.amenities.append(db.session.get(Amenity, 4))
db.session.add(Room(type="presidential suite", price=300000, capacity=10, status="Available", description="description"))
r = db.session.get(Room, 3)
r.amenities.append(db.session.get(Amenity, 1))
r.amenities.append(db.session.get(Amenity, 2))
r.amenities.append(db.session.get(Amenity, 3))
r.amenities.append(db.session.get(Amenity, 4))


#Invoice
db.session.add(Invoice(date=datetime.today(), method="credit card", amount="1000000"))
i = db.session.get(Invoice, 1)
i.services.append(db.session.get(Service, 1))
i.services.append(db.session.get(Service, 3))

#Booking
#db.session.add(Booking(check_in=datetime.today(), check_out=datetime.today(), comment="sadasd", user_id=u.id, room_id=db.session.get(Room, 1).id, invoice_id=i.id))


db.session.commit()
