from typing import List, Optional

# dao
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.transaction_type import TransactionType


class TransactionTypeDAO(BaseDAO[TransactionType]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = TransactionType

        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="transaction_type_id",
        )
