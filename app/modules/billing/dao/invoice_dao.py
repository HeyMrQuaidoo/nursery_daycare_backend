from typing import Optional, List

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.dao.invoice_item_dao import InvoiceItemDAO

# models
from app.modules.billing.models.invoice import Invoice


class InvoiceDAO(BaseDAO[Invoice]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Invoice

        self.invoice_item_dao = InvoiceItemDAO()

        self.detail_mappings = {
            "invoice_items": self.invoice_item_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="invoice_id",
        )
