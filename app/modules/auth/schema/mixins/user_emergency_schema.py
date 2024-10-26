from typing import Annotated, List, Optional
from pydantic import constr, EmailStr

from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.address.schema.address_schema import EmergencyAddressBase

# models
from app.modules.auth.models.user import User as UserModel


class UserEmergencyInfo(BaseSchema, AddressMixin):
    emergency_contact_name: Optional[Annotated[str, constr(max_length=128)]] = None
    emergency_contact_email: Optional[EmailStr] = None
    emergency_contact_relation: Optional[Annotated[str, constr(max_length=128)]] = None
    emergency_contact_number: Optional[Annotated[str, constr(max_length=128)]] = None
    # address: Optional[List[Address] | Address] = None
    address: Optional[List[EmergencyAddressBase]] = []

    @classmethod
    def get_user_emergency_info(cls, user: UserModel):
        return cls(
            emergency_contact_name=user.emergency_contact_name,
            emergency_contact_email=user.emergency_contact_email,
            emergency_contact_relation=user.emergency_contact_relation,
            emergency_contact_number=user.emergency_contact_number,
            address=cls.get_address_base(user.emergency_addresses),
        )
