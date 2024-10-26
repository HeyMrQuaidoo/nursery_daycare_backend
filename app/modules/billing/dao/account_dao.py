from typing import List, Optional

# models
from app.modules.billing.models.account import Account

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO


class AccountDAO(BaseDAO[Account]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Account

        self.address_dao = AddressDAO()
        self.detail_mappings = {
            "address": self.address_dao,
        }
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="account_id",
        )
