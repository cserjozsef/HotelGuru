from __future__ import annotations
from datetime import date
from typing import List
from typing_extensions import Optional
from app.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Date
from sqlalchemy import ForeignKey, Table, Column

InvoiceServices = Table(
    "invserv",
    Base.metadata,
    Column("invoice_id", ForeignKey("invoice_table.id")),
    Column("service_id", ForeignKey("service_table.id"))
)


class Invoice(db.Model):
    __tablename__ = "invoice_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date)
    method: Mapped[str] = mapped_column(String(30))
    amount: Mapped[int]

    booking: Mapped["Booking"] = relationship(back_populates="invoice")

    services: Mapped[Optional[List["Service"]]] = relationship(secondary=InvoiceServices, back_populates="invoices")

    def __repr__(self) -> str:
        return f"Invoice(id={self.id!r}, user_id={self.user_id!s}, booking_id={self.booking_id!r}, date={self.date!r}, method={self.method!r})"
