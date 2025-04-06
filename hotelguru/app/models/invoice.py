from __future__ import annotations
from datetime import date
from typing import List
from sqlalchemy import ForeignKey
from typing_extensions import Optional

from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Date


class Invoice(db.Model):
    __tablename__ = "invoice_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date)
    method: Mapped[str] = mapped_column(String(30))

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="invoice")

    booking: Mapped["Booking"] = relationship(back_populates="invoice")

    service: Mapped[Optional[List["Service"]]] = relationship(back_populates="invoice")

    def __repr__(self) -> str:
        return f"Invoice(id={self.id!r}, user_id={self.user_id!s}, booking_id={self.booking_id!r}, date={self.date!r}, method={self.method!r})"
