from __future__ import annotations
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, Base
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id")),
    Column("role_id", ForeignKey("role_table.id"))
)


class User(db.Model):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    fname: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))

    address_id: Mapped[int] = mapped_column(ForeignKey("address_table.id"))
    address: Mapped["Address"] = relationship(back_populates="user", lazy=True)

    role: Mapped["Role"] = relationship(secondary=UserRole, back_populates="users")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")
    rooms: Mapped[List["Room"]] = relationship(back_populates="user")
    invoice: Mapped["Invoice"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.fname!s}, email={self.email!r})"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
