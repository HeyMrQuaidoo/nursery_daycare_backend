from typing import List

# DAO
from app.modules.contract.dao.contract_type_dao import ContractTypeDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import ContractTypeSchema
from app.modules.contract.schema.contract_type_schema import (
    ContractTypeCreateSchema,
    ContractTypeUpdateSchema,
)


class ContractTypeRouter(BaseCRUDRouter):
    def __init__(
        self, prefix: str = "/contract-type", tags: List[str] = ["ContractType"]
    ):
        # Assign schemas for CRUD operations
        ContractTypeSchema["create_schema"] = ContractTypeCreateSchema
        ContractTypeSchema["update_schema"] = ContractTypeUpdateSchema
        # ContractTypeSchema["response_schema"] = ContractTypeResponse

        # Initialize the DAO for ContractType
        self.dao: ContractTypeDAO = ContractTypeDAO()

        # Call the base class constructor
        super().__init__(
            dao=self.dao, schemas=ContractTypeSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        # Custom route registrations if needed
        pass
