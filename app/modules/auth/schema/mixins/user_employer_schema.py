from typing import Optional

from app.modules.common.schema.base_schema import BaseSchema

# models
from app.modules.auth.models.user import User as UserModel


class UserEmployerInfo(BaseSchema):
    employer_name: Optional[str] = None
    occupation_status: Optional[str] = None
    occupation_location: Optional[str] = None

    @classmethod
    def get_user_employer_info(cls, user: UserModel):
        return cls(
            employer_name=user.employer_name,
            occupation_status=user.occupation_status,
            occupation_location=user.occupation_location,
        )
