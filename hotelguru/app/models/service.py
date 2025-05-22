from __future__ import annotations
from typing import List, Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from app.models.invoice import InvoiceServices


class Service(db.Model):
    __tablename__ = "service_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int]

    invoices: Mapped[Optional[List["Invoice"]]] = relationship(secondary=InvoiceServices, back_populates="services")

    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, booking_id={self.booking_id!s}, type={self.type!r}, price={self.price!r})"
