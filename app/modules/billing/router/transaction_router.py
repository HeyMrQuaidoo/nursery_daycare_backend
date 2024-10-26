from typing import List

# dao
from app.modules.billing.dao.transaction_dao import TransactionDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import TransactionSchema
from app.modules.billing.schema.transaction_schema import (
    TransactionCreateSchema,
    TransactionUpdateSchema,
    TransactionResponse,
)


class TransactionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: TransactionDAO = TransactionDAO(excludes=[])
        TransactionSchema["create_schema"] = TransactionCreateSchema
        TransactionSchema["update_schema"] = TransactionUpdateSchema
        TransactionSchema["response_schema"] = TransactionResponse

        super().__init__(
            dao=self.dao, schemas=TransactionSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
