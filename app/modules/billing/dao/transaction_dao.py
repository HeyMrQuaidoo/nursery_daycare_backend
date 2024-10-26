from typing import Optional, List

# dao
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.transaction import Transaction
from app.modules.billing.dao.invoice_dao import InvoiceDAO
from app.modules.billing.dao.payment_type_dao import PaymentTypeDAO
from app.modules.billing.dao.transaction_type_dao import TransactionTypeDAO
from app.modules.auth.dao.user_dao import UserDAO


class TransactionDAO(BaseDAO[Transaction]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Transaction

        # DAOs for related entities
        self.invoice_dao = InvoiceDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.transaction_type_dao = TransactionTypeDAO()
        self.user_dao = UserDAO()

        # Detail mappings for creating related entities
        self.detail_mappings = {
            "invoice": self.invoice_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="transaction_id",
        )
