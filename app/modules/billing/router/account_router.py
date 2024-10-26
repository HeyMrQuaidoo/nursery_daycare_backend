from typing import List

# dao
from app.modules.billing.dao.account_dao import AccountDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import AccountSchema
from app.modules.billing.schema.account_schema import (
    AccountCreateSchema,
    AccountUpdateSchema,
)


class AccountRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        AccountSchema["create_schema"] = AccountCreateSchema
        AccountSchema["update_schema"] = AccountUpdateSchema
        self.dao: AccountDAO = AccountDAO(excludes=["users"])

        super().__init__(dao=self.dao, schemas=AccountSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
