from __future__ import annotations
from app import db
from app import create_app
from config import Config
from datetime import datetime
from app.models.booking import Booking
from app.models.user import User
from app.models.role import Role
from app.models.room import Room
from app.models.invoice import Invoice
from app.models.service import Service

app = create_app(config_class=Config)
app.app_context().push()


#Role
db.session.add_all([ Role(name="Administrator"),
                     Role(name="Receptionist"),
                     Role(name="Guest")])

#User
user = User( email="email@gmail.com",  address="8100, Veszprém, Egyetem u. 1", fname="Lajos", phone="06121231234")
user.set_password("qweasd")
db.session.add(user)

#Room
db.session.add(Room(type="single", price=30000, occupancy=1, description="Single room etc etc", amenities="air conditioning"))

#Invoice
db.session.add(Invoice(date=datetime.today(), method="cash"))

#Booking
db.session.add(Booking(check_in=datetime.today(), check_out=datetime.today(), days=1))

#Services
db.session.add_all([ Service(name="Massage", price=7000),
                     Service(name="Room Service", price=3000),
                     Service(name="Indoors Pool", price=5000)])

db.session.commit()