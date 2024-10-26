import uuid
from sqlalchemy import Enum, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.billing.enums.billing_enums import AccountTypeEnum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class EntityAccount(Base):
    __tablename__ = "entity_accounts"

    entity_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id")
    )
    account_type: Mapped[AccountTypeEnum] = mapped_column(Enum(AccountTypeEnum))
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))

    __table_args__ = (
        CheckConstraint("entity_type IN ('user')", name="check_entity_type_accounts"),
    )

    account: Mapped["Account"] = relationship(
        "Account", back_populates="entity_accounts", lazy="selectin", overlaps="users"
    )

    @validates("entity_type", "entity_id")
    def validate_entity(self, key, value, **kwargs):
        if key == "entity_id":
            entity_id = value
            entity_type = kwargs.get("entity_type", self.entity_type)
        elif key == "entity_type":
            entity_type = value
            entity_id = self.entity_id

        entity_map = {
            EntityTypeEnum.user: ("users", "user_id"),
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
