from __future__ import annotations
from sqlalchemy import ForeignKey
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer  # vagy Float ha tizedesjegy kell

class Service(db.Model):
    __tablename__ = "service_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("booking_table.id"))
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoice_table.id"))
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer)

    booking: Mapped["Booking"] = relationship(back_populates="services")
    invoice: Mapped["Invoice"] = relationship(back_populates="service")

    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, booking_id={self.booking_id!s}, name={self.name!r}, price={self.price!r})"
