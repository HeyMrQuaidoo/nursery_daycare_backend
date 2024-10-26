from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Any, Optional, List, Union

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum, InvoiceTypeEnum

# schema
from app.modules.auth.schema.mixins.user_mixin import UserBase
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
from app.modules.billing.schema.mixins.invoice_item_mixin import InvoiceItemBase

# model
from app.modules.billing.models.invoice import Invoice as InvoiceModel


class InvoiceBase(BaseSchema):
    issued_by: Optional[Union[UUID | UserBase]] = None
    issued_to: Optional[Union[UUID | UserBase]] = None
    invoice_details: str
    due_date: datetime
    invoice_amount: float
    invoice_type: InvoiceTypeEnum
    status: PaymentStatusEnum
    invoice_items: Optional[List[InvoiceItemBase]]


class Invoice(InvoiceBase):
    invoice_id: UUID
    invoice_number: str


class InvoiceInfoMixin(BaseSchema):
    issued_by: Optional[Union[UUID | UserBase]] = None
    issued_to: Optional[Union[UUID | UserBase]] = None
    invoice_id: Optional[UUID] = None
    invoice_number: str
    invoice_amount: Decimal
    invoice_details: str
    due_date: Optional[datetime]
    date_paid: Optional[datetime]
    invoice_type: Optional[InvoiceTypeEnum]
    status: Optional[PaymentStatusEnum]
    transaction_number: Optional[str]
    invoice_items: Optional[List[InvoiceItemBase]] = []
    # transaction: Optional[TransactionBase] = None
    # contracts: Optional[List[ContractBase]] = []

    _issued_by = str(BaseFaker.uuid4())
    _issued_to = str(BaseFaker.uuid4())
    _invoice_details = BaseFaker.text(max_nb_chars=200)
    _due_date = BaseFaker.future_datetime()
    _invoice_type = BaseFaker.random_element([e.value for e in InvoiceTypeEnum])
    _status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])
    _date_paid = BaseFaker.date_time_this_year()

    _invoice_create_json = {
        "issued_by": _issued_by,
        "issued_to": _issued_to,
        "invoice_details": _invoice_details,
        "due_date": _due_date.isoformat(),
        "invoice_type": _invoice_type,
        "status": _status,
        "invoice_items": [
            {
                "description": BaseFaker.sentence(),
                "quantity": BaseFaker.random_int(min=1, max=10),
                "unit_price": round(BaseFaker.random_number(digits=5), 2),
                "reference_id": str(BaseFaker.uuid4()),
            },
        ],
    }

    _invoice_update_json = {
        "issued_by": _issued_by,
        "issued_to": _issued_to,
        "invoice_details": _invoice_details,
        "due_date": _due_date.isoformat(),
        "date_paid": _date_paid.isoformat(),
        "invoice_type": _invoice_type,
        "status": _status,
    }

    _invoice_response_json = {
        "invoice_id": str(BaseFaker.uuid4()),
        "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
        "issued_by": str(BaseFaker.uuid4()),
        "issued_to": str(BaseFaker.uuid4()),
        "invoice_details": BaseFaker.text(max_nb_chars=200),
        "due_date": BaseFaker.future_datetime().isoformat(),
        "date_paid": BaseFaker.date_time_this_year().isoformat(),
        "invoice_type": BaseFaker.random_element([e.value for e in InvoiceTypeEnum]),
        "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
        "invoice_amount": round(BaseFaker.random_number(digits=5), 2),
        "invoice_items": [
            {
                "invoice_item_id": str(BaseFaker.uuid4()),
                "description": BaseFaker.sentence(),
                "quantity": BaseFaker.random_int(min=1, max=10),
                "unit_price": round(BaseFaker.random_number(digits=5), 2),
                "total_price": round(BaseFaker.random_number(digits=6), 2),
                "reference_id": str(BaseFaker.uuid4()),
            },
        ],
    }

    @classmethod
    def get_invoice_info(cls, invoices: Union[InvoiceModel | List[InvoiceModel] | Any]):
        if isinstance(invoices, list):
            return [cls.model_validate(invoice) for invoice in invoices]
        return cls.model_validate(invoices)

    @classmethod
    def model_validate(cls, invoice: InvoiceModel):
        return cls(
            invoice_id=invoice.invoice_id,
            invoice_number=invoice.invoice_number,
            invoice_amount=invoice.invoice_amount,
            invoice_details=invoice.invoice_details,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            invoice_type=invoice.invoice_type,
            status=invoice.status,
            transaction_number=invoice.transaction_number,
            invoice_items=[
                InvoiceItemBase.model_validate(item) for item in invoice.invoice_items
            ],
            # transaction=TransactionBase.model_validate(invoice.transaction),
            # contracts=[ContractBase.model_validate(contract) for contract in invoice.contracts]
        )
