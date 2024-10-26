from uuid import UUID
from typing import Annotated, List, Optional

from pydantic import EmailStr, constr

# schemas
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.role_mixin import Role


class EmailBody(BaseSchema):
    """
    Model for representing the body of an email.

    Attributes:
        to (EmailStr): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email.
    """

    to: EmailStr
    subject: Annotated[str, constr(max_length=255)]
    message: Annotated[str, constr(max_length=2000)]


class Token(BaseSchema):
    """
    Model for representing a basic token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token, typically 'Bearer'.
    """

    access_token: str
    token_type: str


class TokenExposed(BaseSchema):
    """
    Model for exposing detailed token information.

    Attributes:
        user_id (Optional[UUID]): Optional user ID associated with the token.
        access_token (str): The access token string.
        token_type (str): The type of the token, typically 'Bearer'.
        first_name (str): User's first name.
        email (str): User's email.
        last_name (str): User's last name.
        expires (str): Expiration time of the token.
        roles (List[Role]): List of roles assigned to the user, defaults to an empty list.
    """

    user_id: Optional[UUID] = None
    access_token: str
    token_type: str
    first_name: str
    email: str
    last_name: str
    expires: str
    roles: List[Role] = []


class TokenData(BaseSchema):
    """
    Model for extracting email information from a token.

    Attributes:
        email (Optional[str]): Optional email extracted from the token.
    """

    email: Optional[str] = None


class Login(BaseSchema):
    """
    Model for login request payload.

    Attributes:
        username (str): Username for login.
        password (str): Password for login.
    """

    username: str
    password: str


class ResetPassword(BaseSchema):
    """
    Model for reset password request payload.

    Attributes:
        email (str): Email address to send the reset password link to.
    """

    email: str
