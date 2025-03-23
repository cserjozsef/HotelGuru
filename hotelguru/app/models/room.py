from __future__ import annotations
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class Room(db.Model):
    __tablename__ = "room_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(30))
    price: Mapped[int]
    occupancy: Mapped[int]
    description: Mapped[str] = mapped_column(String(30))
    amenities: Mapped[str] = mapped_column(String(30))

    user: Mapped["User"] = relationship(back_populates="rooms")
    booking: Mapped["Booking"] = relationship(back_populates="room")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, type={self.type!s}, price={self.price!r}, occupancy={self.occupancy!r}, description={self.description!r}, amenities={self.amenities!r})"
