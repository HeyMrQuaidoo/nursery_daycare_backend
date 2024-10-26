from typing import Optional
from pydantic import BaseModel, ConfigDict

# enums
from app.modules.billing.enums.billing_enums import TransactionTypeEnum

# schemas
from app.modules.billing.schema.mixins.transaction_type_mixin import (
    TransactionTypeInfoMixin,
)

# model
from app.modules.billing.models.transaction_type import (
    TransactionType as TransactionTypeModel,
)


class TransactionTypeBase(BaseModel):
    transaction_type_name: TransactionTypeEnum
    transaction_type_description: Optional[str]


class TransactionTypeCreateSchema(TransactionTypeBase, TransactionTypeInfoMixin):
    model_config = ConfigDict(
        json_schema_extra={"example": TransactionTypeInfoMixin._transaction_create_json}
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_id=transaction_type.transaction_type_id,
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()


class TransactionTypeUpdateSchema(TransactionTypeBase, TransactionTypeInfoMixin):
    transaction_type_description: Optional[str] = None
    transaction_type_name: Optional[TransactionTypeEnum] = None  # Enum used here

    model_config = ConfigDict(
        json_schema_extra={"example": TransactionTypeInfoMixin._transaction_update_json}
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_id=transaction_type.transaction_type_id,
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()


class TransactionTypeResponse(TransactionTypeBase, TransactionTypeInfoMixin):
    transaction_type_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": TransactionTypeInfoMixin._transaction_response_json
        },
        from_attributes=True,
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_id=transaction_type.transaction_type_id,
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()
