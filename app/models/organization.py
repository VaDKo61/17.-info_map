from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base

organization_activity_table = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', ForeignKey('activities.id'), primary_key=True),
)


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    phones: Mapped[list['OrganizationPhone']] = relationship(
        'OrganizationPhone', back_populates='organization', cascade='all, delete-orphan'
    )

    building_id: Mapped[int] = mapped_column(ForeignKey('buildings_id'))
    building: Mapped['Building'] = relationship('Building', back_populates='organizations')

    activities: Mapped[list['Activity']] = relationship(
        'Activity',
        secondary=organization_activity_table,
        back_populates='organizations'
    )


class OrganizationPhone(Base):
    __tablename__ = 'organization_phones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship('Organization', back_populates='phones')
