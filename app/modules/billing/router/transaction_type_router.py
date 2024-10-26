from typing import List

# DAO
from app.modules.billing.dao.transaction_type_dao import TransactionTypeDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import TransactionTypeSchema
from app.modules.billing.schema.transaction_type_schema import (
    TransactionTypeCreateSchema,
    TransactionTypeUpdateSchema,
)


class TransactionTypeRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        # Assign schemas for CRUD operations
        TransactionTypeSchema["create_schema"] = TransactionTypeCreateSchema
        TransactionTypeSchema["update_schema"] = TransactionTypeUpdateSchema
        self.dao: TransactionTypeDAO = TransactionTypeDAO()

        # Call the base class constructor
        super().__init__(
            dao=self.dao, schemas=TransactionTypeSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
