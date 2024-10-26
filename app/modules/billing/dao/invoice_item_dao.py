from typing import Optional, List

# dao
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.invoice_item import InvoiceItem


class InvoiceItemDAO(BaseDAO[InvoiceItem]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = InvoiceItem

        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="invoice_item_id",
        )
