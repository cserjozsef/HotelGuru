from __future__ import annotations
from datetime import date
from typing import Optional
from sqlalchemy import ForeignKey
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Date, Integer

class Booking(db.Model):
    __tablename__ = "booking_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    days: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("room_table.id"))
    room: Mapped["Room"] = relationship(back_populates="booking")

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="bookings")

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoice_table.id'))
    invoice: Mapped["Invoice"] = relationship(back_populates="booking")

    def __repr__(self) -> str:
        return (f"Booking(id={self.id!r}, check_in={self.check_in!s}, check_out={self.check_out!r}, "
                f"user_id={self.user_id!r}, room_id={self.room_id!r}, days={self.days!r}, comment={self.comment!r})")
