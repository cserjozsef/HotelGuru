from __future__ import annotations
from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer
import enum

class StatusEnum(enum.Enum):
    Available = 0
    Booked = 1
    Occupied = 2

class Room(db.Model):
    __tablename__ = "room_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)
    status: Mapped[StatusEnum] = mapped_column()
    description: Mapped[str] = mapped_column(String(255))
    amenities: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="rooms")

    def __repr__(self) -> str:
        return (f"Room(id={self.id!r}, type={self.type!r}, price={self.price!r}, "
                f"capacity={self.capacity!r}, status={self.status!r}, "
                f"description={self.description!r}, amenities={self.amenities!r})")
