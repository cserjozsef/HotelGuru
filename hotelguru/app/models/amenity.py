from __future__ import annotations
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from app.models.room import RoomAmenities
from typing import List


class Amenity(db.Model):
    __tablename__ = "amenity_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    rooms: Mapped[List["Room"]] = relationship(secondary=RoomAmenities, back_populates="amenities")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!s})"