from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

from .organization import organization_activity_table


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey('activities.id'), nullable=True)
    parent: Mapped['Activity'] = relationship('Activity', remote_side=[id], back_populates='children')
    children: Mapped[list['Activity']] = relationship('Activity', back_populates='parent')

    organization: Mapped[list['Organization']] = relationship(
        'Organization',
        secondary=organization_activity_table,
        back_populates='activities'
    )
