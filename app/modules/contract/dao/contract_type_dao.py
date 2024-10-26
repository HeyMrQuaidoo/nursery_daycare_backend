from typing import List, Optional

# Models
from app.modules.contract.models.contract_type import ContractType

# DAO
from app.modules.common.dao.base_dao import BaseDAO


class ContractTypeDAO(BaseDAO[ContractType]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = ContractType

        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="contract_type_id",
        )
