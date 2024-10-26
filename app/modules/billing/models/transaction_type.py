from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base

# Enums
from app.modules.billing.enums.billing_enums import TransactionTypeEnum


class TransactionType(Base):
    __tablename__ = "transaction_type"

    transaction_type_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
    )
    transaction_type_name: Mapped[TransactionTypeEnum] = mapped_column(
        Enum(TransactionTypeEnum),
        unique=True,
        index=True,
    )
    transaction_type_description: Mapped[str] = mapped_column(String(128))

    # transactions
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="transaction_types"
    )
