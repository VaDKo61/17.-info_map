from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Building(Base):
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
