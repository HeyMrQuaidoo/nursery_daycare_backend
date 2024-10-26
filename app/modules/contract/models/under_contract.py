import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Enum, UUID, String, event
from datetime import datetime

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum


# TODO (DQ):
# - start_date determined by contract.start_date
# - end_date determined by contract.end_date
# - next_payment_due should be determined by system
class UnderContract(Base):
    __tablename__ = "under_contract"

    under_contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_status: Mapped[ContractStatusEnum] = mapped_column(
        Enum(ContractStatusEnum)
    )
    contract_number: Mapped[str] = mapped_column(
        String(128), ForeignKey("contract.contract_number", ondelete="CASCADE")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    next_payment_due: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # contract
    contract: Mapped["Contract"] = relationship(
        "Contract",
        back_populates="under_contract",
        lazy="selectin",
        foreign_keys=[contract_number],
        viewonly=True,
    )

    # users
    client_representative: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="client_under_contract",
        lazy="selectin",
    )

    employee_representative: Mapped["User"] = relationship(
        "User",
        foreign_keys=[employee_id],
        back_populates="employee_under_contract",
        lazy="selectin",
    )


def parse_dates(mapper, connection, target):
    """Listener to convert start date and date_to to a datetime if it's provided as a string."""
    if isinstance(target.start_date, str):
        # Try to convert 'start date' string to datetime with or without microseconds
        try:
            target.start_date = datetime.strptime(
                target.start_date, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.start_date = datetime.strptime(
                target.start_date, "%Y-%m-%d %H:%M:%S"
            )

    if isinstance(target.end_date, str):
        # Try to convert 'end_date' string to datetime with or without microseconds
        try:
            target.end_date = datetime.strptime(target.end_date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.end_date = datetime.strptime(target.end_date, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.next_payment_due, str):
        # Try to convert 'next_payment_due' string to datetime with or without microseconds
        try:
            target.next_payment_due = datetime.strptime(
                target.next_payment_due, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.next_payment_due = datetime.strptime(
                target.next_payment_due, "%Y-%m-%d %H:%M:%S"
            )


event.listen(UnderContract, "before_insert", parse_dates)
event.listen(UnderContract, "before_update", parse_dates)
