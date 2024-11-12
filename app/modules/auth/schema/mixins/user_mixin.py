from uuid import UUID
from datetime import datetime
from typing import Annotated, Any, Optional
from pydantic import UUID4, Field, constr, EmailStr


# enums
from app.modules.auth.enums.user_enums import GenderEnum

# schema
from app.modules.common.schema.base_schema import BaseSchema

# models
from app.modules.auth.models.user import User as UserModel


class FavoritePropertiesBase(BaseSchema):
    # favorite_id: UUID4
    # user_id: UUID4
    property_unit_assoc_id: UUID4


class UserBase(BaseSchema):
    user_id: Optional[UUID] = None
    first_name: Annotated[str, constr(max_length=128)]
    last_name: Annotated[str, constr(max_length=128)]
    gender: GenderEnum
    date_of_birth: Optional[Any] = Field(
        None,
        alias="date_of_birth",
        description="The date of birth in YYYY-MM-DD format.",
    )
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=50)]
    identification_number: Annotated[str, constr(max_length=80)]
    photo_url: Optional[str] = ""


class UserBaseMixin:
    @classmethod
    def get_user_info(cls, user: UserModel):
        return UserBase(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
            phone_number=user.phone_number,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            date_of_birth=user.date_of_birth,
        )


class UserHiddenFields(BaseSchema):
    # emergency info
    emergency_contact_name: Optional[str] = Field(None, hidden=True)
    emergency_contact_email: Optional[EmailStr] = Field(None, hidden=True)
    emergency_contact_relation: Optional[str] = Field(None, hidden=True)
    emergency_contact_number: Optional[str] = Field(None, hidden=True)

    # auth info
    login_provider: Optional[str] = Field(None, hidden=True)
    reset_token: Optional[str] = Field(None, hidden=True)
    verification_token: Optional[str] = Field(None, hidden=True)
    is_subscribed_token: Optional[str] = Field(None, hidden=True)
    is_disabled: Optional[bool] = Field(None, hidden=True)
    is_verified: Optional[bool] = Field(None, hidden=True)
    is_subscribed: Optional[bool] = Field(None, hidden=True)
    is_approved: Optional[bool] = Field(None, hidden=True)
    is_onboarded: Optional[bool] = Field(None, hidden=True)
    current_login_time: Optional[datetime] = Field(None, hidden=True)
    last_login_time: Optional[datetime] = Field(None, hidden=True)
    password: Optional[str] = Field(None, hidden=True)

    # employer info
    employer_name: Optional[str] = Field(None, hidden=True)
    occupation_status: Optional[str] = Field(None, hidden=True)
    occupation_location: Optional[str] = Field(None, hidden=True)
