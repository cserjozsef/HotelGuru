from __future__ import annotations
from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
import enum


class StatusEnum(enum.Enum):
    Available  = 0,
    Booked  = 1,
    Occupied    = 2

class Room(db.Model):
    __tablename__ = "room_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30))
    price: Mapped[int]
    capacity: Mapped[int]
    status: Mapped[StatusEnum] = mapped_column()
    description: Mapped[str] = mapped_column(String(30))
    amenities: Mapped[str] = mapped_column(String(30))

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="rooms")

    booking_id: Mapped[int] = mapped_column(ForeignKey("booking_table.id"))
    booking: Mapped["Booking"] = relationship(back_populates="room")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, type={self.type!s}, price={self.price!r}, occupancy={self.occupancy!r}, description={self.description!r}, amenities={self.amenities!r})"
