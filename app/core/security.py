import time
import jwt
import bcrypt
from typing import Any
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

from app.core.config import settings
from app.modules.auth.schema.user_schema import UserBase

fernet = Fernet(str.encode(settings.ENCRYPT_KEY))

JWT_ALGORITHM = "HS256"


class Hash:
    def bcrypt(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        return hashed.decode("utf-8")

    def verify(hashed_password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class SecureAccessTokens:
    def token_response(token: str):
        payload: dict = SecureAccessTokens.decode_token(token)
        payload.update({"access_token": token, "token_type": "Bearer"})

        return payload

    def create_access_token(
        subject: UserBase | Any, expires_delta: timedelta = None
    ) -> str:
        ###
        user = subject
        payload = user.to_dict(
            exclude={"password_hash", "updated_at", "created_at", "gender", "user_id"}
        )
        payload = {key: payload[key] for key in payload if key in UserBase.model_fields}
        payload.update({"expires": time.time() + 1800})

        # create the access token with the user's scopes as permissions
        user_permissions = [p.name for r in user.roles for p in r.permissions]
        payload.update({"scope": ",".join(user_permissions)})
        ###

        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        to_encode = {"exp": expire, "sub": str(payload), "type": "access"}
        # to_encode = {"exp": expire, "sub": str(subject), "type": "access"}

        token = jwt.encode(
            payload=to_encode,
            key=settings.ENCRYPT_KEY,
            algorithm=JWT_ALGORITHM,
        )

        # return token
        token_data = SecureAccessTokens.token_response(token)
        token_data.update(
            {
                "first_name": subject.first_name,
                "email": subject.email,
                "user_id": subject.to_dict().get("user_id"),
                "last_name": subject.last_name,
                "expires": payload["expires"],
                "roles": subject.roles,
            }
        )
        return token_data

    def create_refresh_token(
        subject: str | Any, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}

        return jwt.encode(
            payload=to_encode,
            key=settings.ENCRYPT_KEY,
            algorithm=JWT_ALGORITHM,
        )

    def decode_token(token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=settings.ENCRYPT_KEY,
            algorithms=[JWT_ALGORITHM],
        )

    def verify_password(
        plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()

        return bcrypt.checkpw(plain_password, hashed_password)

    def get_password_hash(plain_password: str | bytes) -> str:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        return bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode()

    def get_data_encrypt(data) -> str:
        data = fernet.encrypt(data)
        return data.decode()

    def get_content(variable: str) -> str:
        return fernet.decrypt(variable.encode()).decode()
