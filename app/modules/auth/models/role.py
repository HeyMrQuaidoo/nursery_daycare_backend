import uuid
from typing import List
from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import (
    BaseModel as Base,
    BaseModelCollection,
)


class Role(Base):
    __tablename__ = "role"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(80), unique=True)
    alias: Mapped[str] = mapped_column(String(80), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # users
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_roles", back_populates="roles", lazy="selectin"
    )

    # permissions
    permissions: Mapped[List["Permissions"]] = relationship(
        "Permissions",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin",
    )

    # address
    address: Mapped[List["Addresses"]] = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(Role.role_id==EntityAddress.entity_id, EntityAddress.entity_type=='role')",
        secondaryjoin="and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==False)",
        overlaps="address,entity_addresses,addresses,properties",
        back_populates="roles",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("user_roles", Role)
