from uuid import UUID
from datetime import datetime
from typing import List, Optional


# schemas
from app.modules.common.schema.base_schema import BaseSchema, BaseFaker
from app.modules.billing.schema.mixins.billable_mixin import EntityBillable

# models
from app.modules.billing.models.utility import Utilities as UtilitiesModel
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel
from app.modules.associations.models.entity_billable import (
    EntityBillable as EntityBillableModel,
)


class UtilityBase(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    billable_type: Optional[str] = None
    billable_amount: Optional[int] = None
    apply_to_units: Optional[bool] = False
    payment_type_id: Optional[int] = (None,)
    start_period: Optional[datetime] = None
    end_period: Optional[datetime] = None
    billable_id: Optional[UUID] = None


class Utility(BaseSchema):
    name: str
    description: Optional[str] = None


class UtilityInfo(BaseSchema):
    utility: str
    frequency: str
    billable_amount: float
    apply_to_units: bool
    entity_billable_id: UUID


class UtilitiesMixin:
    _name = BaseFaker.word()
    _description = BaseFaker.sentence()

    _utility_create_json = {
        "name": _name,
        "description": _description,
    }

    _utility_update_json = {
        "name": _name,
        "description": _description,
    }

    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]):
        """
        Get utilities information.

        Args:
            utilities (List[EntityBillable]): List of entity billable objects.

        Returns:
            List[Dict[str, Any]]: List of utility information.
        """
        result = []

        for entity_utility in utilities:
            entity_utility: EntityBillableModel = entity_utility
            payment_type: PaymentTypeModel = entity_utility.payment_type
            utility: UtilitiesModel = entity_utility.utility

            print("erlekjrl")
            result.append(
                UtilityInfo(
                    utility=utility.name,
                    frequency=payment_type.payment_type_name,
                    billable_amount=entity_utility.billable_amount,
                    apply_to_units=entity_utility.apply_to_units,
                    entity_billable_id=entity_utility.entity_billable_id,
                )
            )

        return result
