from __future__ import annotations
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, Base
from sqlalchemy import ForeignKey, Table, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Kapcsolótábla a user-roles many-to-many kapcsolatnak
UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("role_id", ForeignKey("role_table.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    fname: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)

    address_id: Mapped[int] = mapped_column(ForeignKey("address_table.id"))
    address: Mapped["Address"] = relationship(back_populates="user", lazy="joined")

    roles: Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates="users")

    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")

    rooms: Mapped[List["Room"]] = relationship(back_populates="user")

    invoices: Mapped[List["Invoice"]] = relationship(back_populates="user")

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.fname} ({self.email})>"
