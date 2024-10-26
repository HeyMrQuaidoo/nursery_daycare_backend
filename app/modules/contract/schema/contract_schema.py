from uuid import UUID
from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# Enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# Schema
from app.modules.billing.schema.mixins.utility_mixin import UtilitiesMixin
from app.modules.contract.schema.mixins.contract_mixin import (
    ContractBase,
    ContractInfoMixin,
)

# Models
from app.modules.contract.models.contract import Contract as ContractModel


class ContractCreateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    contract_number: Optional[str] = None
    contract_id: Optional[UUID] = None

    model_config = ConfigDict(
        json_schema_extra={"example": ContractInfoMixin._contract_create_json},
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            invoices=cls.get_invoices_info(contract.invoices),
            under_contract=cls.get_contract_details(contract.under_contract),
            media=cls.get_media_info(contract.media),
        ).model_dump()


class ContractUpdateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    contract_type_id: Optional[int] = None
    payment_type_id: Optional[int] = None
    contract_status: Optional[ContractStatusEnum] = None
    contract_details: Optional[str] = None
    num_invoices: Optional[int] = None
    payment_amount: Optional[Decimal] = None
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={"example": ContractInfoMixin._contract_update_json},
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            invoices=cls.get_invoices_info(contract.invoices),
            under_contract=cls.get_contract_details(contract.under_contract),
            media=cls.get_media_info(contract.media),
        ).model_dump()


class ContractResponse(ContractBase, ContractInfoMixin):
    contract_id: UUID
    contract_number: str

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            invoices=cls.get_invoices_info(contract.invoices),
            contract_info=cls.get_contract_details(contract.under_contract),
            media=cls.get_media_info(contract.media),
        ).model_dump(exclude=["client_id", "employee_id"])
