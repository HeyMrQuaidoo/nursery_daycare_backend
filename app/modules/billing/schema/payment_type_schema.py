from typing import Optional
from pydantic import ConfigDict

# enums
from app.modules.billing.enums.billing_enums import PaymentTypeEnum

# schemas
from app.modules.billing.schema.mixins.payment_type_mixin import (
    PaymentTypeBase,
    PaymentTypeInfoMixin,
)

# models
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel


class PaymentTypeCreateSchema(PaymentTypeBase, PaymentTypeInfoMixin):
    model_config = ConfigDict(
        json_schema_extra={"example": PaymentTypeInfoMixin._payment_create_json}
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_id=payment_type.payment_type_id,
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()


class PaymentTypeUpdateSchema(PaymentTypeBase, PaymentTypeInfoMixin):
    payment_partitions: Optional[int] = None
    payment_type_description: Optional[str] = None
    payment_type_name: Optional[PaymentTypeEnum] = None  # Enum used here

    model_config = ConfigDict(
        json_schema_extra={"example": PaymentTypeInfoMixin._payment_update_json}
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()


class PaymentTypeResponse(PaymentTypeBase):
    payment_type_id: int

    model_config = ConfigDict(
        json_schema_extra={"example": PaymentTypeInfoMixin._payment_response_json},
        from_attributes=True,
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_id=payment_type.payment_type_id,
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()
