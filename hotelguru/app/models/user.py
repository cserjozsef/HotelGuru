from __future__ import annotations
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class User(db.Model):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    fname: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(30))

    role: Mapped["Role"] = relationship(back_populates="role_table.user")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="booking_table.user")
    rooms: Mapped[List["Room"]] = relationship(back_populates="room_table.user")
    invoice: Mapped["Invoice"] = relationship(back_populates="invoice_table.user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.fname!s}, email={self.email!r})"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
