from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# enums
from app.modules.auth.enums.user_enums import GenderEnum

# schema
from app.modules.address.schema.address_schema import AddressCreateSchema


class UserSchema(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    identification_number: str
    photo_url: Optional[str] = None
    gender: GenderEnum
    date_of_birth: Optional[datetime] = None
    login_provider: Optional[str] = "native"
    reset_token: Optional[str] = None
    verification_token: Optional[str] = None
    is_subscribed_token: Optional[str] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime
    last_login_time: Optional[datetime] = None
    employer_name: Optional[str] = None
    occupation_status: Optional[str] = None
    occupation_location: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_email: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    # emergency_address_hash: UUID

    # roles: Optional[List[RoleSchema]] = []
    # address: Optional[List[AddressCreateSchema]] = []

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )


class UserCreateSchema(BaseModel):
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr
    phone_number: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    identification_number: str = Field(..., max_length=80)
    photo_url: Optional[str] = Field(None, max_length=128)
    gender: GenderEnum
    date_of_birth: Optional[str] = None
    login_provider: Optional[str] = "native"
    reset_token: Optional[str] = None
    verification_token: Optional[str] = None
    is_subscribed_token: Optional[str] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = Field(default_factory=datetime.now)
    last_login_time: Optional[datetime] = None
    employer_name: Optional[str] = Field(None, max_length=128)
    occupation_status: Optional[str] = Field(None, max_length=128)
    occupation_location: Optional[str] = Field(None, max_length=128)
    emergency_contact_name: Optional[str] = Field(None, max_length=128)
    emergency_contact_email: Optional[str] = Field(None, max_length=128)
    emergency_contact_relation: Optional[str] = Field(None, max_length=128)
    emergency_contact_number: Optional[str] = Field(None, max_length=128)
    # emergency_address_hash: Optional[UUID] = None
    address: Optional[List[AddressCreateSchema]] = None

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )
