from __future__ import annotations
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from app.models.user import UserRole
from typing import List


class Role(db.Model):
    __tablename__ = "role_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    users: Mapped[List["User"]] = relationship(secondary=UserRole, back_populates="roles")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!s})"