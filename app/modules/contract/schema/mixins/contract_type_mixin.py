from decimal import Decimal
from typing import Any, List, Optional, Union

# enums
from app.modules.contract.enums.contract_enums import ContractTypeEnum

# schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
from app.modules.contract.schema.mixins.contract_mixin import ContractBase

# models
from app.modules.contract.models.contract_type import ContractType as ContractTypeModel


class ContractTypeBase(BaseSchema):
    fee_percentage: Decimal
    contract_type_name: ContractTypeEnum
    contracts: Optional[List[ContractBase]] = []


class ContractType(BaseSchema):
    contract_type_id: Optional[int] = None


class ContractTypeInfoMixin:
    _contract_type_name = BaseFaker.random_element([e.value for e in ContractTypeEnum])
    _fee_percentage = round(BaseFaker.random_number(digits=3), 2)

    _contract_type_create_json = {
        "contract_type_name": _contract_type_name,
        "fee_percentage": _fee_percentage,
    }

    _contract_type_update_json = {
        "contract_type_name": _contract_type_name,
        "fee_percentage": _fee_percentage,
    }

    @classmethod
    def get_contract_type_info(
        cls, contract_types: Union[ContractTypeModel | List[ContractTypeModel] | Any]
    ):
        if isinstance(contract_types, list):
            return [
                cls.model_validate(contract_type) for contract_type in contract_types
            ]
        return cls.model_validate(contract_types)

    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_id=contract_type.contract_type_id,
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
            contracts=[
                ContractBase.model_validate(contract)
                for contract in contract_type.contracts
            ],
        )
