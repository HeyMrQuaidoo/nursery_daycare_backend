from datetime import datetime
from typing import Annotated, Optional
from pydantic import constr

from app.modules.common.schema.base_schema import BaseSchema

# models
from app.modules.auth.models.user import User as UserModel


class UserAuthInfo(BaseSchema):
    login_provider: Optional[Annotated[str, constr(max_length=128)]] = None
    reset_token: Optional[Annotated[str, constr(max_length=128)]] = None
    verification_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_subscribed_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = datetime.now()
    last_login_time: Optional[datetime] = None

    @classmethod
    def get_user_auth_info(cls, user: UserModel):
        return cls(
            login_provider=user.login_provider,
            reset_token=user.reset_token,
            verification_token=user.verification_token,
            is_subscribed_token=user.is_subscribed_token,
            is_disabled=user.is_disabled,
            is_verified=user.is_verified,
            is_subscribed=user.is_subscribed,
            current_login_time=user.current_login_time,
            last_login_time=user.last_login_time,
        )


class UserAuthCreateInfo(BaseSchema):
    password: Optional[str] = ""
    login_provider: Optional[Annotated[str, constr(max_length=128)]] = None
    reset_token: Optional[Annotated[str, constr(max_length=128)]] = None
    verification_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_subscribed_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = datetime.now()
    last_login_time: Optional[datetime] = None
