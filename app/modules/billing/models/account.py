import uuid
from typing import List
from sqlalchemy import String, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bank_account_name: Mapped[str] = mapped_column(String(80))
    bank_account_number: Mapped[str] = mapped_column(String(80))
    account_branch_name: Mapped[str] = mapped_column(String(80))

    # users
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="entity_accounts",
        primaryjoin="and_(EntityAccount.account_id==Account.account_id, EntityAccount.entity_type=='user')",
        secondaryjoin="EntityAccount.entity_id==User.user_id",
        back_populates="accounts",
        lazy="selectin",
    )

    # entity_accounts
    entity_accounts: Mapped[List["EntityAccount"]] = relationship(
        "EntityAccount", back_populates="account", lazy="selectin", overlaps="users"
    )

    # address
    address: Mapped[List["Addresses"]] = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(Account.account_id==EntityAddress.entity_id, EntityAddress.entity_type=='account')",
        secondaryjoin="and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==False)",
        overlaps="address,entity_addresses,addresses,properties",
        back_populates="accounts",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("accounts", Account)
