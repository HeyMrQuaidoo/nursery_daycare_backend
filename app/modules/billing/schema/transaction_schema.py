from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum

# mixins
from app.modules.billing.schema.mixins.invoice_mixin import InvoiceBase
from app.modules.billing.schema.mixins.transaction_mixin import (
    TransactionBase,
    TransactionInfoMixin,
)

# models
from app.modules.billing.models.transaction import Transaction as TransactionModel


class TransactionCreateSchema(TransactionBase, TransactionInfoMixin):
    invoice: Optional[InvoiceBase] = None
    model_config = ConfigDict(
        json_schema_extra={"example": TransactionInfoMixin._transaction_create_json},
    )

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        print(f"DO I EVER REACH HERE: {transaction}")

        return cls(
            transaction_id=transaction.transaction_id,
            transaction_number=transaction.transaction_number,
            transaction_details=transaction.transaction_details,
            transaction_status=transaction.transaction_status,
            payment_type_id=transaction.payment_type_id,
            transaction_type=transaction.transaction_type
            if transaction.transaction_type
            else None,
            transaction_date=transaction.transaction_date,
            invoice_number=transaction.invoice_number
            if transaction.invoice_number
            else None,
            client_offered=transaction.client_offered
            if transaction.client_offered
            else None,
            client_requested=transaction.client_requested
            if transaction.client_requested
            else None,
            invoice=transaction.invoice,
        ).model_dump()


class TransactionUpdateSchema(TransactionBase):
    payment_type_id: Optional[int] = None
    client_offered: Optional[UUID] = None
    client_requested: Optional[UUID] = None
    transaction_date: Optional[datetime] = None
    transaction_details: Optional[str] = None
    transaction_type: Optional[int] = None
    transaction_status: Optional[PaymentStatusEnum] = None
    invoice_number: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": TransactionInfoMixin._transaction_update_json},
    )


class TransactionResponse(TransactionBase, TransactionInfoMixin):
    transaction_id: UUID
    transaction_number: str

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        return cls(
            transaction_id=transaction.transaction_id,
            transaction_number=transaction.transaction_number,
            transaction_details=transaction.transaction_details,
            transaction_status=transaction.transaction_status,
            payment_type_id=transaction.payment_type_id,
            transaction_type=transaction.transaction_type
            if transaction.transaction_type
            else None,
            transaction_date=transaction.transaction_date,
            invoice_number=transaction.invoice_number
            if transaction.invoice_number
            else None,
            client_offered=transaction.client_offered
            if transaction.client_offered
            else None,
            client_requested=transaction.client_requested
            if transaction.client_requested
            else None,
            invoice=transaction.invoice,
        ).model_dump()
