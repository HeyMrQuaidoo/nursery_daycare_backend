from typing import Optional, List

# enums
from app.modules.billing.enums.billing_enums import TransactionTypeEnum

# schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
from app.modules.billing.schema.transaction_schema import TransactionBase

# models
from app.modules.billing.models.transaction_type import (
    TransactionType as TransactionTypeModel,
)


class TransactionTypeBase(BaseSchema):
    transaction_type_id: Optional[int] = None
    transaction_type_name: TransactionTypeEnum
    transaction_type_description: str
    transactions: Optional[List[TransactionBase]] = []


class TransactionTypeInfoMixin:
    _transaction_type_name = BaseFaker.random_element(
        [e.value for e in TransactionTypeEnum]
    )
    _transaction_type_description = BaseFaker.sentence()
    _transaction_type_id = BaseFaker.random_int(min=1, max=100)

    _transaction_create_json = {
        "transaction_type_name": _transaction_type_name,
        "transaction_type_description": _transaction_type_description,
    }

    _transaction_update_json = {
        "transaction_type_name": _transaction_type_name,
        "transaction_type_description": _transaction_type_description,
    }

    _transaction_response_json = {
        "transaction_type_id": _transaction_type_id,
        "transaction_type_name": _transaction_type_name,
        "transaction_type_description": _transaction_type_description,
    }

    @classmethod
    def get_transaction_type_info(
        cls, transaction_types: TransactionTypeModel | list[TransactionTypeModel]
    ):
        if isinstance(transaction_types, list):
            return [
                cls.model_validate(transaction_type)
                for transaction_type in transaction_types
            ]
        return cls.model_validate(transaction_types)

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_id=transaction_type.transaction_type_id,
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
            transactions=[
                TransactionBase.model_validate(transaction)
                for transaction in transaction_type.transactions
            ],
        )
