from uuid import UUID
from typing import Any, Optional
from datetime import datetime

# enums
from app.modules.billing.enums.billing_enums import (
    InvoiceTypeEnum,
    PaymentStatusEnum,
)

# schemas
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
from app.modules.billing.schema.mixins.invoice_mixin import InvoiceBase

# models
from app.modules.billing.models.transaction import Transaction as TransactionModel


class TransactionBase(BaseSchema):
    payment_type_id: int
    client_offered: UUID
    client_requested: UUID
    transaction_date: datetime
    transaction_details: str
    transaction_type: int
    transaction_status: PaymentStatusEnum
    invoice_number: Optional[str] = None
    invoice: Optional[InvoiceBase | Any] = None


class Transaction(BaseSchema):
    transaction_id: UUID
    transaction_number: str


class TransactionInfoMixin:
    _payment_type_id = BaseFaker.random_int(min=1, max=1)
    _client_offered = str(BaseFaker.uuid4())
    _client_requested = str(BaseFaker.uuid4())
    _transaction_date = BaseFaker.date_time_this_year()
    _transaction_details = BaseFaker.text(max_nb_chars=200)
    _transaction_type = BaseFaker.random_int(min=1, max=1)
    _transaction_status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])
    _invoice_number = f"INV{BaseFaker.random_number(digits=8)}"

    _transaction_create_json = {
        "payment_type_id": _payment_type_id,
        "client_offered": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
        "client_requested": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
        "transaction_date": _transaction_date.isoformat(),
        "transaction_details": _transaction_details,
        "transaction_type": _transaction_type,
        "transaction_status": _transaction_status,
        "invoice": {
            "issued_by": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
            "issued_to": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
            "invoice_details": BaseFaker.text(max_nb_chars=200),
            "invoice_amount": round(BaseFaker.random_number(digits=2), 2),
            "due_date": BaseFaker.future_datetime().isoformat(),
            "invoice_type": BaseFaker.random_element(
                [e.value for e in InvoiceTypeEnum]
            ),
            "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
            "invoice_items": [
                {
                    "description": BaseFaker.sentence(),
                    "quantity": BaseFaker.random_int(min=1, max=10),
                    "unit_price": round(BaseFaker.random_number(digits=5), 2),
                    "reference_id": str(BaseFaker.uuid4()),
                }
            ],
        },
    }

    _transaction_update_json = {
        "payment_type_id": _payment_type_id,
        "client_offered": _client_offered,
        "client_requested": _client_requested,
        "transaction_date": _transaction_date.isoformat(),
        "transaction_details": _transaction_details,
        "transaction_type": _transaction_type,
        "transaction_status": _transaction_status,
        "invoice_number": _invoice_number,
        "invoice": {
            "issued_by": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
            "issued_to": "1ae69b5f-b1fb-4974-a2ba-e7162fd29412",
            "invoice_details": BaseFaker.text(max_nb_chars=200),
            "invoice_amount": round(BaseFaker.random_number(digits=2), 2),
            "due_date": BaseFaker.future_datetime().isoformat(),
            "invoice_type": BaseFaker.random_element(
                [e.value for e in InvoiceTypeEnum]
            ),
            "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
            "invoice_items": [
                {
                    "invoice_item_id": str(BaseFaker.uuid4()),
                    "description": BaseFaker.sentence(),
                    "quantity": BaseFaker.random_int(min=1, max=10),
                    "unit_price": round(BaseFaker.random_number(digits=5), 2),
                    "reference_id": str(BaseFaker.uuid4()),
                }
            ],
        },
    }

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        """
        This method should only use the data in the `TransactionModel` object and should not call `get_transaction_info` again to avoid recursion.
        """
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
        )

    @classmethod
    def get_transaction_info(cls, transaction: TransactionModel) -> dict:
        """
        Return a dictionary representation of transaction info, but do not call `model_validate` inside.
        """
        return {
            "transaction_id": transaction.transaction_id,
            "transaction_number": transaction.transaction_number,
            "transaction_details": transaction.transaction_details,
            "transaction_status": transaction.transaction_status,
            "payment_type_id": transaction.payment_type_id,
            "transaction_type": transaction.transaction_type
            if transaction.transaction_type
            else None,
            "transaction_date": transaction.transaction_date,
            "invoice_number": transaction.invoice_number
            if transaction.invoice_number
            else None,
            "client_offered": transaction.client_offered
            if transaction.client_offered
            else None,
            "client_requested": transaction.client_requested
            if transaction.client_requested
            else None,
        }
