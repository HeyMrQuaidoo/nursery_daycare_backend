from uuid import UUID
from typing import Optional
from pydantic import ConfigDict

# schemas
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.billing.schema.mixins.billable_mixin import (
    BillableBase,
    EntityBillable,
)

# models
from app.modules.associations.models.entity_billable import (
    EntityBillable as EntityBillableModel,
)


class BillableCreateSchema(BillableBase):
    billable_assoc_id: Optional[UUID] = None
    billable_type: str

    # Faker attributes
    _billable_type = BaseFaker.random_element(["service", "product", "subscription"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "billable_assoc_id": str(BaseFaker.uuid4()),
                "billable_type": _billable_type,
            }
        }
    )


class BillableUpdateSchema(BillableBase):
    billable_assoc_id: Optional[UUID] = None
    billable_type: Optional[str]

    # Faker attributes
    _billable_type = BaseFaker.random_element(["service", "product", "subscription"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "billable_assoc_id": str(BaseFaker.uuid4()),
                "billable_type": _billable_type,
            }
        }
    )


class BillableResponseSchema(BillableBase):
    billable_assoc_id: Optional[UUID] = None
    billable_type: str

    # Faker attributes
    _billable_type = BaseFaker.random_element(["service", "product", "subscription"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "billable_assoc_id": str(BaseFaker.uuid4()),
                "billable_type": _billable_type,
            }
        }
    )

    class EntityBillableCreateSchema(EntityBillable):
        # Faker attributes
        _entity_type = BaseFaker.random_element(
            ["company", "individual", "organization"]
        )
        _billable_type = BaseFaker.random_element(
            ["service", "product", "subscription"]
        )
        _billable_amount = BaseFaker.random_int(min=100, max=10000)

        model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "payment_type_id": BaseFaker.random_int(min=1, max=5),
                    "entity_id": str(BaseFaker.uuid4()),
                    "entity_type": _entity_type,
                    "billable_id": str(BaseFaker.uuid4()),
                    "billable_type": _billable_type,
                    "billable_amount": _billable_amount,
                    "apply_to_units": BaseFaker.boolean(),
                    "start_period": BaseFaker.date_this_year(),
                    "end_period": BaseFaker.future_date(),
                }
            }
        )

        @classmethod
        def model_validate(cls, entity_billable: EntityBillableModel):
            return cls(
                entity_billable_id=entity_billable.entity_billable_id,
                payment_type_id=entity_billable.payment_type_id,
                entity_id=entity_billable.entity_id,
                entity_type=entity_billable.entity_type,
                billable_id=entity_billable.billable_id,
                billable_type=entity_billable.billable_type,
                billable_amount=entity_billable.billable_amount,
                apply_to_units=entity_billable.apply_to_units,
            )


class EntityBillableUpdateSchema(EntityBillable):
    _entity_type = BaseFaker.random_element(["company", "individual", "organization"])
    _billable_type = BaseFaker.random_element(["service", "product", "subscription"])
    _billable_amount = BaseFaker.random_int(min=100, max=10000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_id": BaseFaker.random_int(min=1, max=5),
                "entity_id": str(BaseFaker.uuid4()),
                "entity_type": _entity_type,
                "billable_id": str(BaseFaker.uuid4()),
                "billable_type": _billable_type,
                "billable_amount": _billable_amount,
                "apply_to_units": BaseFaker.boolean(),
                "start_period": BaseFaker.date_this_year(),
                "end_period": BaseFaker.future_date(),
            }
        }
    )

    @classmethod
    def model_validate(cls, entity_billable: EntityBillableModel):
        return cls(
            entity_billable_id=entity_billable.entity_billable_id,
            payment_type_id=entity_billable.payment_type_id,
            entity_id=entity_billable.entity_id,
            entity_type=entity_billable.entity_type,
            billable_id=entity_billable.billable_id,
            billable_type=entity_billable.billable_type,
            billable_amount=entity_billable.billable_amount,
            apply_to_units=entity_billable.apply_to_units,
        )


class EntityBillableResponseSchema(EntityBillable):
    _entity_type = BaseFaker.random_element(["company", "individual", "organization"])
    _billable_type = BaseFaker.random_element(["service", "product", "subscription"])
    _billable_amount = BaseFaker.random_int(min=100, max=10000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_id": BaseFaker.random_int(min=1, max=5),
                "entity_id": str(BaseFaker.uuid4()),
                "entity_type": _entity_type,
                "billable_id": str(BaseFaker.uuid4()),
                "billable_type": _billable_type,
                "billable_amount": _billable_amount,
                "apply_to_units": BaseFaker.boolean(),
                "start_period": BaseFaker.date_this_year(),
                "end_period": BaseFaker.future_date(),
            }
        }
    )

    @classmethod
    def model_validate(cls, entity_billable: EntityBillableModel):
        return cls(
            entity_billable_id=entity_billable.entity_billable_id,
            payment_type_id=entity_billable.payment_type_id,
            entity_id=entity_billable.entity_id,
            entity_type=entity_billable.entity_type,
            billable_id=entity_billable.billable_id,
            billable_type=entity_billable.billable_type,
            billable_amount=entity_billable.billable_amount,
            apply_to_units=entity_billable.apply_to_units,
        )
