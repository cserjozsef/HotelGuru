from __future__ import annotations
from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

class Address(db.Model):
    __tablename__ = "address_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(30))
    street: Mapped[str] = mapped_column(String(30))
    postalcode: Mapped[str] = mapped_column(String(10))  # String típus, hogy megőrizzük a vezető nullákat

    user: Mapped["User"] = relationship(back_populates="address")
