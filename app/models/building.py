from typing import TYPE_CHECKING

from core.database import Base
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .organization import Organization


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    address: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        unique=True,
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="building"
    )
