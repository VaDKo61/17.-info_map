from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    phones: Mapped[list['OrganizationPhone']] = relationship(
        'OrganizationPhone', back_populates='organization', cascade='all, delete-orphan'
    )


class OrganizationPhone(Base):
    __tablename__ = 'organization_phones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship('Organization', back_populates='phones')
