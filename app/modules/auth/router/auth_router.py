import uuid
import asyncio
from typing import List, Union
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.modules.auth.models.user import User

# daos
from app.modules.auth.dao.user_dao import UserDAO
from app.modules.auth.dao.auth_dao import AuthDAO

# services
from app.services.email_service import EmailService

# routers
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import UserSchema
from app.modules.auth.schema.auth_schema import Login, ResetPassword

RESET_LINK = "https://housekee.netlify.app/account-recovery?token={}"
UNSUBSCRIBE_LINK = (
    "https://hskee-hsm-backend-test/auth/mail-unsubscribe?email={}&token={}"
)


class AuthRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: AuthDAO = AuthDAO()
        self.user_dao: UserDAO = UserDAO()
        super().__init__(
            dao=self.dao,
            schemas=UserSchema,
            prefix=prefix,
            tags=tags,
            show_default_routes=False,
        )

        self.register_routes()

    def register_routes(self):
        @self.router.post("/")
        async def user_login(request: Login, db: AsyncSession = Depends(self.get_db)):
            current_user: User = await self.user_dao.user_exists(
                db_session=db, email=request.username
            )

            if current_user is None:
                raise HTTPException(status_code=401, detail="User not found")

            if current_user.is_verified and (
                current_user.login_provider == "native"
                or current_user.login_provider is None
            ):
                if current_user.password is None:
                    raise HTTPException(
                        status_code=401, detail="Please set your password first!"
                    )

                if await self.dao.verify_password(db_session=db, login_info=request):
                    current_user.update_last_login_time()

                    return await self.dao.authenticate_user(current_user=current_user)
                else:
                    raise HTTPException(status_code=401, detail="Wrong login details!")
            else:
                raise HTTPException(
                    status_code=401,
                    detail="User account not verified or using a login provider",
                )

        @self.router.post("/reset-password")
        async def reset_password(
            request: ResetPassword, db: AsyncSession = Depends(self.get_db)
        ):
            current_user: Union[User, None] = await self.user_dao.user_exists(
                db_session=db, email=request.email
            )

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")

            if not current_user.reset_token and current_user.password is not None:
                current_user.reset_token = str(uuid.uuid4())
                current_user.is_subscribed_token = str(uuid.uuid4())
                current_user.password = None
                email_service = EmailService()

                response = await self.dao.commit_and_refresh(
                    db_session=db, obj=current_user
                )

                asyncio.create_task(
                    email_service.send_reset_password_email(
                        current_user.email,
                        current_user.first_name + " " + current_user.last_name,
                        RESET_LINK.format(current_user.reset_token),
                        UNSUBSCRIBE_LINK.format(
                            current_user.email, current_user.is_subscribed_token
                        ),
                    )
                )

                if response:
                    return {"data": "User password reset!"}
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="User account not verified or using a login provider",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="User account not verified or using a login provider",
                )

        @self.router.get("/verify-email")
        async def verify_email(
            email: str, token: str, db: AsyncSession = Depends(self.get_db)
        ):
            current_user: Union[User, None] = await self.user_dao.user_exists(
                db_session=db, email=email
            )

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")

            if (
                not current_user.is_verified
                and current_user.verification_token == token
            ):
                current_user.is_verified = True
                current_user.verification_token = None
                response = await self.dao.commit_and_refresh(
                    db_session=db, obj=current_user
                )

                if response:
                    return {"data": "User successfully verified!"}
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="User account not verified or using a login provider",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="User account not verified or using a login provider",
                )

        @self.router.get("/mail-unsubscribe")
        async def mail_unsubscribe(
            email: str, token: str, db: AsyncSession = Depends(self.get_db)
        ):
            current_user: Union[User, None] = await self.user_dao.user_exists(
                db_session=db, email=email
            )

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")

            if current_user.is_subscribed and current_user.is_subscribed_token == token:
                current_user.is_subscribed = False
                current_user.is_subscribed_token = None
                response = await self.dao.commit_and_refresh(
                    db_session=db, obj=current_user
                )

                if response:
                    return {"data": "User successfully unsubsribed!"}
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="User account not verified or using a login provider",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="User account not verified or using a login provider",
                )

        @self.router.get("/mail-subscribe")
        async def mail_subscribe(
            email: str, token: str, db: AsyncSession = Depends(self.get_db)
        ):
            current_user: Union[User, None] = await self.user_dao.user_exists(
                db_session=db, email=email
            )

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")

            if (
                not current_user.is_subscribed
                and current_user.is_subscribed_token == token
            ):
                current_user.is_subscribed = True
                current_user.is_subscribed_token = None
                response = await self.dao.commit_and_refresh(
                    db_session=db, obj=current_user
                )

                if response:
                    return {"data": "User successfully subsribed!"}
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="User account not verified or using a login provider",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="User account not verified or using a login provider",
                )
