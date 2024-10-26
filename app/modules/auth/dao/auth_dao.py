from typing import Union
from fastapi import Request
from fastapi_sso.sso.base import OpenID
from fastapi_sso.sso.google import GoogleSSO
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.modules.auth.models.user import User

# daos
from app.modules.auth.dao.user_dao import UserDAO
from app.modules.common.dao.base_dao import BaseDAO

# utils
from app.core.security import Hash, SecureAccessTokens
from app.core.config import settings
from app.core.response import DAOResponse
# from app.utils.jwt.auth_handler import signJWT

# schemas
from app.modules.auth.schema.auth_schema import Login, TokenExposed

CLIENT_ID = settings.GOOGLE_SIGNIN_CLIENT_ID
CLIENT_SECRET = settings.GOOGLE_SIGNIN_CLIENT_SECRET

google_sso = GoogleSSO(CLIENT_ID, CLIENT_SECRET, settings.GOOGLE_CALLBACK)


class AuthDAO(BaseDAO[User]):
    def __init__(self):
        self.model = User
        self.user_dao = UserDAO()

        super().__init__(self.model)

    async def google_login(self):
        with google_sso:
            return await google_sso.get_login_redirect()

    async def google_callback(self, db_session: AsyncSession, request: Request):
        with google_sso:
            try:
                user: OpenID = await google_sso.verify_and_process(request)

                existing_user: User = await self.user_dao.user_exists(
                    db_session, user.email
                )

                if existing_user:
                    if not existing_user.is_verified:
                        raise Exception("User account not verified")

                    existing_user.update_last_login_time()

                    # return signJWT(existing_user)
                    return SecureAccessTokens.create_access_token(existing_user)
                else:
                    # create a new user if not found
                    created_user = await self.create_google_user(db_session, user)
                    # return signJWT(created_user)
                    return SecureAccessTokens.create_access_token(created_user)

            except Exception as e:
                return DAOResponse[str](
                    success=True, data=f"Google Sign-In failed: {str(e)}"
                )

    async def create_google_user(self, db_session: AsyncSession, user: OpenID) -> User:
        """
        Creates a new user based on Google account information.
        """
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": "",
            "password_hash": "",
            "date_of_birth": "",
            "is_verified": False,
            "login_provider": user.provider,
            "gender": "male",
        }
        created_user: User = await self.user_dao.create(
            db_session=db_session, obj_in=user_data
        )
        created_user.update_last_login_time()

        return created_user

    async def verify_password(
        self, db_session: AsyncSession, login_info: Login
    ) -> bool:
        """
        Verifies a user's password against the stored hash.
        """
        current_user: Union[User | None] = await self.user_dao.user_exists(
            db_session=db_session, email=login_info.username
        )

        if current_user is None:
            raise NoResultFound("User does not exist")

        return Hash.verify(current_user.password, login_info.password)

    async def authenticate_user(self, current_user: User) -> DAOResponse[TokenExposed]:
        # return signJWT(current_user)
        return SecureAccessTokens.create_access_token(current_user)
