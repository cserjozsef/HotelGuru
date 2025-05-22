from __future__ import annotations
from app.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey, Column, Table
from typing import List, Optional


RoomAmenities = Table(
    "roomamen",
    Base.metadata,
    Column("room_id", ForeignKey("room_table.id")),
    Column("amenity_id", ForeignKey("amenity_table.id"))
)


class Room(db.Model):
    __tablename__ = "room_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30))
    price: Mapped[int]
    capacity: Mapped[int]
    status: Mapped[String] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))

    amenities: Mapped[List["Amenity"]] = relationship(secondary=RoomAmenities, back_populates="rooms")
    booking: Mapped[Optional["Booking"]] = relationship(back_populates="room")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, type={self.type!s}, price={self.price!r}, occupancy={self.occupancy!r}, description={self.description!r}, amenities={self.amenities!r})"
