from uuid import UUID
from typing import Optional
from pydantic import ConfigDict

# schemas
from app.modules.billing.schema.mixins.invoice_item_mixin import (
    InvoiceItemBase,
    InvoiceItemMixin,
)

# models
from app.modules.billing.models.invoice_item import InvoiceItem as InvoiceItemModel


class InvoiceItemCreateSchema(InvoiceItemBase, InvoiceItemMixin):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": InvoiceItemMixin._invoice_create_json},
    )


class InvoiceItemUpdateSchema(InvoiceItemBase, InvoiceItemMixin):
    invoice_number: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    description: Optional[str] = None
    reference_id: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": InvoiceItemMixin._invoice_update_json},
    )


class InvoiceItemResponse(InvoiceItemMixin):
    invoice_item_id: Optional[UUID] = None

    @classmethod
    def model_validate(cls, invoice_item: InvoiceItemModel):
        return cls.get_invoice_item_info(invoice_item)
