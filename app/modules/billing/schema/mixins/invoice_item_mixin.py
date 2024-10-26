from uuid import UUID
from decimal import Decimal
from typing import Any, List, Optional, Union

# schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# models
from app.modules.billing.models.invoice_item import InvoiceItem as InvoiceItemModel


class InvoiceItemBase(BaseSchema):
    quantity: int
    unit_price: Decimal
    total_price: Decimal = None
    description: Optional[str] = None
    reference_id: Optional[str] = None
    invoice_number: Optional[str] = None


class InvoiceItem(InvoiceItemBase):
    invoice_item_id: Optional[UUID] = None
    total_price: float


class InvoiceItemMixin(InvoiceItemBase):
    invoice_item_id: Optional[UUID] = None
    invoice_number: str
    total_price: float

    _quantity = BaseFaker.random_int(min=1, max=100)
    _unit_price = round(BaseFaker.random_number(digits=5), 2)
    _description = BaseFaker.text(max_nb_chars=200)

    _invoice_create_json = {
        "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
        "quantity": _quantity,
        "unit_price": _unit_price,
        "total_price": _quantity * _unit_price,
        "description": _description,
        "reference_id": str(BaseFaker.uuid4()),
    }

    _invoice_update_json = {
        "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
        "quantity": _quantity,
        "unit_price": _unit_price,
        "total_price": _quantity * _unit_price,
        "description": _description,
        "reference_id": str(BaseFaker.uuid4()),
    }

    @classmethod
    def get_invoice_item_info(
        cls, invoice_items: Union[InvoiceItemModel | List[InvoiceItemModel] | Any]
    ):
        if isinstance(invoice_items, list):
            return [cls.model_validate(item) for item in invoice_items]
        return cls.model_validate(invoice_items)

    @classmethod
    def model_validate(cls, item: InvoiceItemModel):
        return cls(
            invoice_item_id=item.invoice_item_id,
            invoice_number=item.invoice_number,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price,
            description=item.description,
            reference_id=item.reference_id,
        )
