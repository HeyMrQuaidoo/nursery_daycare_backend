from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# schemas
from app.modules.auth.schema.user_schema import UserBase
from app.modules.contract.schema.mixins.contract_mixin import ContractBase
from app.modules.contract.schema.mixins.under_contract_mixin import (
    UnderContractBase,
    UnderContractInfoMixin,
)

# models
from app.modules.contract.models.under_contract import (
    UnderContract as UnderContractModel,
)


class UnderContractCreateSchema(UnderContractBase, UnderContractInfoMixin):
    property_unit_assoc_id: UUID
    contract_status: ContractStatusEnum
    contract_number: Optional[str] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    next_payment_due: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": UnderContractInfoMixin._under_contract_create_json
        }
    )


class UnderContractUpdateSchema(UnderContractBase):
    property_unit_assoc_id: Optional[UUID] = None
    contract_status: Optional[ContractStatusEnum] = None
    contract_number: Optional[str] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    next_payment_due: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": UnderContractInfoMixin._under_contract_update_json
        }
    )


class UnderContractResponse(UnderContractBase):
    @classmethod
    def model_validate(cls, under_contract: UnderContractModel):
        return cls(
            under_contract_id=under_contract.under_contract_id,
            contract_status=under_contract.contract_status,
            contract_number=under_contract.contract_number,
            client_id=under_contract.client_id,
            employee_id=under_contract.employee_id,
            start_date=under_contract.start_date,
            end_date=under_contract.end_date,
            next_payment_due=under_contract.next_payment_due,
            contract=ContractBase.model_validate(under_contract.contract)
            if under_contract.contract
            else None,
            client_representative=UserBase.model_validate(
                under_contract.client_representative
            )
            if under_contract.client_representative
            else None,
            employee_representative=UserBase.model_validate(
                under_contract.employee_representative
            )
            if under_contract.employee_representative
            else None,
        ).model_dump()
