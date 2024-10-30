from typing import List
from sqlalchemy import func
from sqlalchemy.future import select
from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.modules.auth.dao.user_dao import UserDAO

# models
from app.modules.auth.models.user import User

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import UserSchema
from app.modules.auth.schema.user_schema import UserCreateSchema, UserUpdateSchema

# core
from app.core.response import DAOResponse
from app.core.errors import CustomException, RecordNotFoundException, IntegrityError


class UserRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: UserDAO = UserDAO(excludes=[""])
        UserSchema["create_schema"] = UserCreateSchema
        UserSchema["update_schema"] = UserUpdateSchema

        super().__init__(dao=self.dao, schemas=UserSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        @self.router.get("/stats/")
        async def get_user_stats(db_session: AsyncSession = Depends(self.get_db)):
            # Query for the count of registered users (is_verified=True and is_onboarded=True)
            registered_query = select(func.count(User.user_id)).where(
                User.is_verified == True,  # noqa E712
                User.is_onboarded == True,  # noqa E712
            )
            registered_count_result = await db_session.execute(registered_query)
            registered_count = registered_count_result.scalar()

            # Query for the count of users with is_onboarded=False
            not_onboarded_query = select(func.count(User.user_id)).where(
                User.is_onboarded == False  # noqa E712
            )
            not_onboarded_count_result = await db_session.execute(not_onboarded_query)
            not_onboarded_count = not_onboarded_count_result.scalar()

            # Query for the count of active users (is_active=True)
            active_users_query = select(func.count(User.user_id)).where(
                User.is_disabled == False,  # noqa E712
                User.is_onboarded == True,  # noqa E712
            )
            active_users_count_result = await db_session.execute(active_users_query)
            active_users_count = active_users_count_result.scalar()

            stats = {
                "registered_users": registered_count,
                "not_onboarded_users": not_onboarded_count,
                "active_users": active_users_count,
            }

            return (
                stats
                if isinstance(stats, DAOResponse)
                else DAOResponse(success=True, data=stats)
            )

        @self.router.get("/admitted/")
        async def admitted_users(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            try:
                admitted_users = await self.dao.query(
                    db_session, filters={"is_verified": True}
                )
                if not admitted_users:
                    raise RecordNotFoundException(model=self.model_schema.__name__)

                meta = await self.dao.build_pagination_meta(
                    request=request,
                    limit=limit,
                    offset=offset,
                    db_session=db_session,
                    filter_condition={"is_verified": True},
                )

                if isinstance(admitted_users, DAOResponse):
                    if hasattr(admitted_users, "meta") and getattr(
                        admitted_users, "meta"
                    ):
                        meta_data = admitted_users.meta
                        meta.update(meta_data)
                    admitted_users.set_meta(meta)

                return (
                    admitted_users
                    if isinstance(admitted_users, DAOResponse)
                    else DAOResponse(success=True, data=admitted_users, meta=meta)
                )
            except RecordNotFoundException:
                return DAOResponse(success=True, data=[])
            except IntegrityError as e:
                raise CustomException(e)
            except Exception as e:
                raise CustomException(e)
