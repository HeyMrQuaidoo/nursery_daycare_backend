import uuid
from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class ContractInvoice(Base):
    __tablename__ = "contract_invoice"

    contract_invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contract.contract_id")
    )
    invoice_number: Mapped[str] = mapped_column(
        String(128), ForeignKey("invoice.invoice_number")
    )
