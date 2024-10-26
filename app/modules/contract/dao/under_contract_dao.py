from typing import Optional, List

# Base DAO and related imports
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.contract.models.under_contract import UnderContract
# from app.modules.properties.dao.property_unit_assoc_dao import PropertyUnitAssocDAO
# from app.modules.auth.dao.user_dao import UserDAO


class UnderContractDAO(BaseDAO[UnderContract]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = UnderContract

        # DAOs for related entities
        # self.user_dao = UserDAO()
        # Assuming we are mapping a user to a contract and at the same time want to map it to a property
        # self.property_unit_assoc_dao = PropertyUnitAssocDAO()

        # Detail mappings to resolve relationships
        self.detail_mappings = {
            # "properties": self.property_unit_assoc_dao,
            # "client_representative": self.user_dao,
        }

        # Call the base DAO with appropriate arguments
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="under_contract_id",
        )
