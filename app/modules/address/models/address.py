import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UUID, Boolean, Enum, String, ForeignKey

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.address.enums.address_enums import AddressTypeEnum


class Addresses(Base):
    __tablename__ = "address"

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    address_type: Mapped[AddressTypeEnum] = mapped_column(Enum(AddressTypeEnum))
    primary: Mapped[bool] = mapped_column(Boolean, default=True)
    address_1: Mapped[str] = mapped_column(String(80))
    address_2: Mapped[str] = mapped_column(String(80))
    address_postalcode: Mapped[str] = mapped_column(String(20))
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("city.city_id")
    )
    region_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("region.region_id")
    )
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.country_id")
    )

    city: Mapped["City"] = relationship(
        "City", back_populates="addresses", lazy="joined"
    )
    region: Mapped["Region"] = relationship(
        "Region", back_populates="addresses", lazy="joined"
    )
    country: Mapped["Country"] = relationship(
        "Country", back_populates="addresses", lazy="joined"
    )

    entity_addresses: Mapped["EntityAddress"] = relationship(
        "EntityAddress",
        # overlaps="users,properties,rental_history",
        backref="address",
        viewonly=True,
    )

    users: Mapped["User"] = relationship(
        "User",
        secondary="entity_address",
        primaryjoin="EntityAddress.address_id==Addresses.address_id",
        secondaryjoin="and_(EntityAddress.entity_id==User.user_id, EntityAddress.entity_type=='user')",
        back_populates="address",
        lazy="selectin",
        viewonly=True,
    )

    roles: Mapped["Role"] = relationship(
        "Role",
        secondary="entity_address",
        primaryjoin="EntityAddress.address_id==Addresses.address_id",
        secondaryjoin="and_(EntityAddress.entity_id==Role.role_id, EntityAddress.entity_type=='role')",
        back_populates="address",
        lazy="selectin",
        viewonly=True,
    )

    accounts: Mapped["Account"] = relationship(
        "Account",
        secondary="entity_address",
        primaryjoin="EntityAddress.address_id==Addresses.address_id",
        secondaryjoin="and_(EntityAddress.entity_id==Account.account_id, EntityAddress.entity_type=='account')",
        back_populates="address",
        lazy="selectin",
        viewonly=True,
    )


# register model
Base.setup_model_dynamic_listener("entity_address", Addresses)
