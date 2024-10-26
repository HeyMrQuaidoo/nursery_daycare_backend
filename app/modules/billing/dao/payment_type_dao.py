from typing import List, Optional

# dao
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.payment_type import PaymentType


class PaymentTypeDAO(BaseDAO[PaymentType]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = PaymentType

        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="payment_type_id",
        )
