from typing import List
from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.modules.auth.dao.user_dao import UserDAO

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
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)
