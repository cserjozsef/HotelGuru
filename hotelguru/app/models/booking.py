from __future__ import annotations
from datetime import date
from typing import List, Optional
from sqlalchemy import ForeignKey
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Date


class Booking(db.Model):
    __tablename__ = "booking_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room_table.id"))
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    days: Mapped[int]
    comment: Mapped[Optional[str]] = mapped_column(String(30))

    room: Mapped["Room"] = relationship(back_populates="room_table.booking")
    user: Mapped[List["User"]] = relationship(back_populates="bookings")
    invoice: Mapped["Invoice"] = relationship(back_populates="invoice_table.booking")

    def __repr__(self) -> str:
        return f"Booking(id={self.id!r}, check_in={self.check_in!s}, check_out={self.check_out!r}, user_id={self.user_id!r}, room_id={self.room_id!r}, days={self.days!r} , comment={self.comment!r})"
