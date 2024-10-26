import uuid
from typing import Optional
from importlib import import_module
from sqlalchemy.orm import relationship, Session, Mapped, mapped_column
from sqlalchemy import String, event, Integer, Numeric, ForeignKey, UUID

# models
from app.modules.common.models.model_base import BaseModel as Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    invoice_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    invoice_number: Mapped[str] = mapped_column(
        String(128), ForeignKey("invoice.invoice_number"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reference_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # invoice
    invoice: Mapped["Invoice"] = relationship(
        "Invoice", back_populates="invoice_items", lazy="selectin"
    )


@event.listens_for(InvoiceItem, "before_insert")
@event.listens_for(InvoiceItem, "before_update")
def calculate_total_price(mapper, connection, target: InvoiceItem):
    # calculate the total price as unit_price * quantity
    target.total_price = target.unit_price * target.quantity


@event.listens_for(InvoiceItem, "after_insert")
@event.listens_for(InvoiceItem, "after_update")
@event.listens_for(InvoiceItem, "after_delete")
def update_invoice_after_item_change(mapper, connection, target: InvoiceItem):
    # update the invoice amount when an invoice item is added, updated, or deleted
    models_module = import_module("app.modules.billing.models.invoice")
    invoice_model = getattr(models_module, "Invoice")

    session = Session(connection)
    invoice = (
        session.query(invoice_model)
        .filter_by(invoice_number=target.invoice_number)
        .first()
    )

    if invoice:
        total_amount = sum(item.total_price for item in invoice.invoice_items)
        connection.execute(
            invoice.__table__.update()
            .where(invoice.__table__.c.invoice_number == invoice.invoice_number)
            .values(invoice_amount=total_amount)
        )
    session.close()


# register model
Base.setup_model_dynamic_listener("invoice_items", InvoiceItem)
