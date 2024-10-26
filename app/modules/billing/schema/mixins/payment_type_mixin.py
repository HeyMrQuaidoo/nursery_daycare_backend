from typing import Any, List, Optional, Union

# schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
# from app.modules.contract.schema.contract_schema import ContractBase
# from app.modules.billing.schema.transaction_schema import TransactionBase

# models
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel
from app.modules.billing.enums.billing_enums import PaymentTypeEnum


class PaymentTypeBase(BaseSchema):
    payment_type_id: Optional[int] = None
    payment_type_name: PaymentTypeEnum
    payment_type_description: str
    payment_partitions: int
    # contracts: Optional[List[ContractBase]] = []
    # transactions: Optional[List[TransactionBase]] = []
    # entity_billable: Optional[List[EntityBillableBase]] = []


class PaymentType(PaymentTypeBase):
    payment_type_id: Optional[int] = None


class PaymentTypeInfoMixin:
    # base attributes
    _payment_type_id = BaseFaker.random_int(min=1, max=100)
    _payment_type_name = BaseFaker.random_element([e.value for e in PaymentTypeEnum])
    _payment_partitions = BaseFaker.random_int(min=1, max=12)
    _payment_type_description = BaseFaker.sentence()

    _payment_create_json = {
        "payment_type_name": _payment_type_name,
        "payment_type_description": _payment_type_description,
        "payment_partitions": _payment_partitions,
    }

    _payment_update_json = {
        "payment_type_name": _payment_type_name,
        "payment_type_description": _payment_type_description,
        "payment_partitions": _payment_partitions,
    }

    _payment_response_json = {
        "payment_type_id": _payment_type_id,
        "payment_type_name": _payment_type_name,
        "payment_type_description": _payment_type_description,
        "payment_partitions": _payment_partitions,
    }

    @classmethod
    def get_payment_type_info(
        cls, payment_types: Union[PaymentTypeModel | List[PaymentTypeModel] | Any]
    ):
        if isinstance(payment_types, list):
            return [cls.model_validate(payment_type) for payment_type in payment_types]
        return cls.model_validate(payment_types)

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_id=payment_type.payment_type_id,
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
            # contracts=[ContractBase.model_validate(contract) for contract in payment_type.contracts],
            # transactions=[TransactionBase.model_validate(transaction) for transaction in payment_type.transactions],
            # entity_billable=[EntityBillableBase.model_validate(billable) for billable in payment_type.entity_billable]
        )
