import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from sqlalchemy import (
    Boolean,
    Integer,
    Enum,
    CheckConstraint,
    Numeric,
    UUID,
    ForeignKey,
    DateTime,
)

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.billing.enums.billing_enums import BillableTypeEnum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class EntityBillable(Base):
    __tablename__ = "entity_billable"

    entity_billable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    entity_type: Mapped[EntityTypeEnum] = mapped_column(
        Enum(EntityTypeEnum), nullable=False
    )

    billable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billable_assoc.billable_assoc_id"),
        nullable=False,
    )
    billable_type: Mapped[BillableTypeEnum] = mapped_column(
        Enum(BillableTypeEnum), nullable=False
    )
    billable_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    apply_to_units: Mapped[bool] = mapped_column(Boolean, default=False)

    payment_type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("payment_type.payment_type_id"), nullable=True
    )

    start_period: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    end_period: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('contract')",
            name="check_entity_type_billables",
        ),
    )

    # Relationships
    payment_type: Mapped[Optional["PaymentType"]] = relationship(
        "PaymentType", back_populates="entity_billable", lazy="selectin"
    )

    contract: Mapped[Optional["Contract"]] = relationship(
        "Contract",
        primaryjoin="and_(EntityBillable.entity_id == Contract.contract_id, "
        "EntityBillable.entity_type == 'contract')",
        foreign_keys="[EntityBillable.entity_id]",
        back_populates="entity_billables",
        overlaps="entity_billables",
        lazy="selectin",
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
            EntityTypeEnum.contract: (
                "contract",
                "contract_id",
            ),
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
