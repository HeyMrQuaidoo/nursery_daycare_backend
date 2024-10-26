import uuid
import pytz
from datetime import datetime
from importlib import import_module
from sqlalchemy.orm import relationship, Session, Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    UUID,
    event,
    inspect,
)

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum

# models
from app.modules.common.models.model_base import BaseModel as Base
from app.modules.common.models.model_base_collection import BaseModelCollection


class Transaction(Base):
    __tablename__ = "transaction"
    TRN_PREFIX = "TRN"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    transaction_number: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )
    payment_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("payment_type.payment_type_id")
    )
    client_offered: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    client_requested: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    transaction_details: Mapped[str] = mapped_column(Text)
    transaction_type: Mapped[int] = mapped_column(
        Integer, ForeignKey("transaction_type.transaction_type_id")
    )
    transaction_status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum)
    )
    invoice_number: Mapped[str] = mapped_column(
        String(128),
        ForeignKey(
            "invoice.invoice_number",
            use_alter=True,
            name="fk_transaction_invoice_number",
        ),
        nullable=True,
    )

    # payment_type
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", back_populates="transactions", lazy="selectin"
    )

    # transaction_type
    transaction_types: Mapped["TransactionType"] = relationship(
        "TransactionType", back_populates="transactions"
    )

    # users
    client_offered_transaction: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_offered],
        back_populates="transaction_as_client_offered",
        lazy="selectin",
    )
    client_requested_transaction: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_requested],
        back_populates="transaction_as_client_requested",
        lazy="selectin",
    )

    # invoice
    invoice: Mapped["Invoice"] = relationship(
        "Invoice",
        primaryjoin="Invoice.invoice_number==Transaction.invoice_number",
        back_populates="transaction",
        lazy="selectin",
        collection_class=BaseModelCollection,
    )


@event.listens_for(Transaction, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.transaction_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.transaction_number = f"{Transaction.TRN_PREFIX}{current_time_str}"


@event.listens_for(Transaction, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.transaction_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.transaction_number = f"{Transaction.TRN_PREFIX}{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.transaction_id == target.transaction_id)
            .values(transaction_number=target.transaction_number)
        )


@event.listens_for(Transaction, "after_update")
def update_transaction_number_on_invoice(mapper, connection, target):
    # Check if the invoice_number is set on the Transaction object
    state = inspect(target)

    if state.attrs.invoice_number.history.has_changes():
        models_module = import_module("app.modules.billing.models.invoice")
        invoice_model = getattr(models_module, "Invoice")

        # session = Session.object_session(target)  # Get the current session
        session = Session(connection)
        # Query the Invoice model to find the related invoice
        invoice = (
            session.query(invoice_model)
            .filter_by(invoice_number=target.invoice_number)
            .first()
        )

        if invoice:
            # Update the transaction_number on the Invoice
            invoice.transaction_number = target.transaction_number

            # Commit the changes to the database
            session.commit()
        session.close()


# register model
Base.setup_model_dynamic_listener("transaction", Transaction)
