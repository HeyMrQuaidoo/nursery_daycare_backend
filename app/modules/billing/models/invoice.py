import uuid
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Numeric, ForeignKey, DateTime, Enum, String, Text, UUID, event

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum, InvoiceTypeEnum


class Invoice(Base):
    __tablename__ = "invoice"
    INVOICE_PREFIX: str = "INV"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    invoice_number: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )
    issued_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", use_alter=True, name="fk_invoice_issued_by"),
    )
    issued_to: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", use_alter=True, name="fk_invoice_issued_to"),
    )
    invoice_details: Mapped[str] = mapped_column(Text)
    invoice_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    date_paid: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    invoice_type: Mapped[InvoiceTypeEnum] = mapped_column(
        Enum(InvoiceTypeEnum), default=InvoiceTypeEnum.general
    )
    status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending
    )
    transaction_number: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("transaction.transaction_number", ondelete="CASCADE"),
        nullable=True,
    )

    # contracts
    contracts: Mapped[list["Contract"]] = relationship(
        "Contract", secondary="contract_invoice", back_populates="invoices"
    )

    # transactions
    transaction: Mapped["Transaction"] = relationship(
        "Transaction",
        primaryjoin="Invoice.invoice_number==Transaction.invoice_number",
        back_populates="invoice",
        lazy="selectin",
    )

    # invoice_items
    invoice_items: Mapped[list["InvoiceItem"]] = relationship(
        "InvoiceItem",
        back_populates="invoice",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # users
    issued_by_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[issued_by],
        backref="invoice_as_issued_by_user",
        lazy="selectin",
    )
    issued_to_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[issued_to],
        backref="invoice_as_issued_to_user",
        lazy="selectin",
    )


@event.listens_for(Invoice, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.invoice_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.invoice_number = f"{Invoice.INVOICE_PREFIX}{current_time_str}"


@event.listens_for(Invoice, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.invoice_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.invoice_number = f"{Invoice.INVOICE_PREFIX}{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.invoice_id == target.invoice_id)
            .values(invoice_number=target.invoice_number)
        )


@event.listens_for(Invoice, "after_insert")
@event.listens_for(Invoice, "after_update")
def update_invoice_amount(mapper, connection, target):
    total_amount = sum(item.total_price for item in target.invoice_items)
    connection.execute(
        target.__table__.update()
        .where(target.__table__.c.invoice_id == target.invoice_id)
        .values(invoice_amount=total_amount)
    )


def parse_dates(mapper, connection, target):
    """Listener to convert date_paid and date_to to a datetime if it's provided as a string."""
    if isinstance(target.date_paid, str):
        # Try to convert 'date_paid' string to datetime with or without microseconds
        try:
            target.date_paid = datetime.strptime(
                target.date_paid, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.date_paid = datetime.strptime(target.date_paid, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.due_date, str):
        # Try to convert 'due_date' string to datetime with or without microseconds
        try:
            target.due_date = datetime.strptime(target.due_date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.due_date = datetime.strptime(target.due_date, "%Y-%m-%d %H:%M:%S")


event.listen(Invoice, "before_insert", parse_dates)
event.listen(Invoice, "before_update", parse_dates)

# register model
Base.setup_model_dynamic_listener("invoice", Invoice)
