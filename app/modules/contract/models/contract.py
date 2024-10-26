import uuid
import pytz
from typing import List
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column, column_property
from sqlalchemy import (
    Numeric,
    String,
    event,
    ForeignKey,
    DateTime,
    Enum,
    Integer,
    Text,
    UUID,
    select,
)

# models
from app.modules.common.models.model_base import BaseModel as Base
from app.modules.common.models.model_base_collection import BaseModelCollection
from app.modules.contract.models.contract_type import ContractType
from app.modules.billing.models.payment_type import PaymentType

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum


class Contract(Base):
    __tablename__ = "contract"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_number: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )
    contract_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("contract_type.contract_type_id")
    )  # [one_time, monthly, quarterly, semi_annual, annual]
    payment_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("payment_type.payment_type_id")
    )
    contract_status: Mapped[ContractStatusEnum] = mapped_column(
        Enum(ContractStatusEnum)
    )
    contract_details: Mapped[str] = mapped_column(Text)
    num_invoices: Mapped[int] = mapped_column(Integer, default=0)
    payment_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    fee_percentage: Mapped[float] = mapped_column(Numeric(5, 2))
    fee_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    date_signed: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )

    # invoices
    invoices: Mapped[List["Invoice"]] = relationship(
        "Invoice",
        secondary="contract_invoice",
        back_populates="contracts",
        lazy="selectin",
    )

    # contract
    under_contract: Mapped[List["UnderContract"]] = relationship(
        "UnderContract",
        back_populates="contract",
        lazy="selectin",
        foreign_keys="UnderContract.contract_number",
        cascade="all, delete-orphan",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # billable
    entity_billables: Mapped[List["EntityBillable"]] = relationship(
        "EntityBillable",
        primaryjoin="foreign(EntityBillable.entity_id) == Contract.contract_id",
        back_populates="contract",
        overlaps="entity_billables,property,utilities,",
        lazy="selectin",
        collection_class=BaseModelCollection,
    )

    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="and_(Contract.contract_id == EntityMedia.entity_id, EntityMedia.entity_type == 'contract')",
        secondaryjoin="EntityMedia.media_id == Media.media_id",
        viewonly=True,
        lazy="selectin",
        collection_class=BaseModelCollection,
    )

    # contract_type
    contract_type: Mapped["ContractType"] = relationship(
        "ContractType", back_populates="contracts", lazy="selectin"
    )

    # payment_type
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", back_populates="contracts", lazy="selectin"
    )

    # generate dynamic column property
    contract_type_value = column_property(
        select(ContractType.contract_type_name)
        .where(ContractType.contract_type_id == contract_type_id)
        .correlate_except(ContractType)
        .scalar_subquery()
    )

    payment_type_value = column_property(
        select(PaymentType.payment_type_name)
        .where(PaymentType.payment_type_id == payment_type_id)
        .correlate_except(PaymentType)
        .scalar_subquery()
    )

    def to_dict(self, exclude=[]):
        if exclude is None:
            exclude = set()
        data = {}

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if key == "contract_type_id":
                    data["contract_type_value"] = str(self.contract_type)
                    continue
                if key == "payment_type_id":
                    data["payment_type_value"] = str(self.payment_type)
                    continue
                if isinstance(value, uuid.UUID):
                    value = str(value)
                data[key] = value

        return data


@event.listens_for(Contract, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.contract_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.contract_number = f"CTR{current_time_str}"


@event.listens_for(Contract, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.contract_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.contract_number = f"CTR{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.contract_id == target.contract_id)
            .values(contract_number=target.contract_number)
        )


# Register model outside the class definition
Base.setup_model_dynamic_listener("contract", Contract)
