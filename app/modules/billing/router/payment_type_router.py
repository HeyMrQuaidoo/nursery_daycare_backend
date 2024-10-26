from typing import List

# DAO
from app.modules.billing.dao.payment_type_dao import PaymentTypeDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import PaymentTypeSchema
from app.modules.billing.schema.payment_type_schema import (
    PaymentTypeCreateSchema,
    PaymentTypeUpdateSchema,
)


class PaymentTypeRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        # Assign schemas for CRUD operations
        PaymentTypeSchema["create_schema"] = PaymentTypeCreateSchema
        PaymentTypeSchema["update_schema"] = PaymentTypeUpdateSchema
        self.dao: PaymentTypeDAO = PaymentTypeDAO()

        # Call the base class constructor
        super().__init__(
            dao=self.dao, schemas=PaymentTypeSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
