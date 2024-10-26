from typing import List
from sqlalchemy import Integer, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.billing.enums.billing_enums import PaymentTypeEnum
from app.modules.common.models.model_base import BaseModel as Base


class PaymentType(Base):
    __tablename__ = "payment_type"

    payment_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, index=True
    )
    payment_type_name: Mapped[PaymentTypeEnum] = mapped_column(Enum(PaymentTypeEnum))
    payment_type_description: Mapped[str] = mapped_column(Text)
    payment_partitions: Mapped[int] = mapped_column(Integer)

    # contracts
    contracts: Mapped[List["Contract"]] = relationship(
        "Contract", back_populates="payment_type"
    )

    # transactions
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="payment_type"
    )

    # billables
    entity_billable: Mapped[List["EntityBillable"]] = relationship(
        "EntityBillable", back_populates="payment_type"
    )
