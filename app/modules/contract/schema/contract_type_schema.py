from typing import Optional
from decimal import Decimal
from pydantic import ConfigDict

# enum
from app.modules.contract.enums.contract_enums import ContractTypeEnum

# schemas
from app.modules.contract.schema.mixins.contract_type_mixin import (
    ContractTypeBase,
    ContractTypeInfoMixin,
)

# models
from app.modules.contract.models.contract_type import ContractType as ContractTypeModel


class ContractTypeCreateSchema(ContractTypeBase, ContractTypeInfoMixin):
    model_config = ConfigDict(
        json_schema_extra={"example": ContractTypeInfoMixin._contract_type_create_json}
    )

    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()


class ContractTypeUpdateSchema(ContractTypeBase, ContractTypeInfoMixin):
    fee_percentage: Optional[Decimal] = None
    contract_type_name: Optional[ContractTypeEnum] = None

    model_config = ConfigDict(
        json_schema_extra={"example": ContractTypeInfoMixin._contract_type_update_json}
    )

    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()


class ContractTypeResponse(ContractTypeBase):
    contract_type_id: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_id=contract_type.contract_type_id,
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()
