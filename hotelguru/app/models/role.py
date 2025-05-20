from __future__ import annotations
from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from app.models.user import UserRole

class Role(db.Model):
    __tablename__ = "role_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(secondary=UserRole, back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"
