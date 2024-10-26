import inspect
from uuid import UUID
from functools import partial
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar, Generic, Union
from fastapi import APIRouter, Depends, Query, Request, status

# dao
from app.modules.common.dao.base_dao import BaseDAO

# schema
from app.modules.common.schema.base_schema import SchemasDictType

# core
from app.core.lifespan import get_db
from app.core.response import DAOResponse
from app.core.errors import CustomException, RecordNotFoundException, IntegrityError


DBModelType = TypeVar("DBModelType")


class BaseCRUDRouter(Generic[DBModelType]):
    def __init__(
        self,
        dao: BaseDAO[DBModelType],
        schemas: SchemasDictType,
        prefix: str = "",
        tags: List[str] = [],
        show_default_routes=True,
    ):
        self.dao = dao
        self.model_pk = schemas["primary_keys"]
        self.model_schema = schemas["model_schema"]
        self.create_schema = schemas["create_schema"]
        self.update_schema = schemas["update_schema"]
        self.get_db = get_db
        self.router = APIRouter(prefix=prefix, tags=tags)

        if show_default_routes:
            self.add_get_all_route()
            self.add_get_route()
            self.add_create_route()
            self.add_update_route()
            self.add_delete_route()

    def add_get_all_route(self):
        @self.router.get("/")
        async def get_all(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            try:
                items = await self.dao.get_all(
                    db_session=db_session, offset=offset, limit=limit
                )

                # if not items:
                #     raise RecordNotFoundException(msg="No Record found")

                meta = await self.dao.build_pagination_meta(
                    request=request, limit=limit, offset=offset, db_session=db_session
                )

                if isinstance(items, DAOResponse):
                    if hasattr(items, "meta") and getattr(items, "meta"):
                        meta_data = items.meta
                        meta.update(meta_data)
                    items.set_meta(meta)

                return (
                    items
                    if isinstance(items, DAOResponse)
                    else DAOResponse(success=True, data=items, meta=meta)
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)

    def add_get_route(self):
        @self.router.get("/{id}")
        async def get(
            id: Union[UUID, str], db_session: AsyncSession = Depends(get_db)
        ) -> DAOResponse:
            try:
                item = await self.dao.get(db_session=db_session, id=id)

                if not item:
                    raise RecordNotFoundException(
                        model=self.model_schema.__name__, id=id
                    )

                return (
                    item
                    if isinstance(item, DAOResponse)
                    else DAOResponse(
                        success=True,
                        data=item,
                    )
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)

    def add_create_route(self):
        @self.router.post("/", status_code=status.HTTP_201_CREATED)
        async def create(
            item: self.create_schema, db_session: AsyncSession = Depends(get_db)
        ) -> DAOResponse:
            try:
                created_item = await self.dao.create(db_session=db_session, obj_in=item)
                # determine how to call model_validate
                method = getattr(self.create_schema, "model_validate")
                signature = inspect.signature(method)

                if "for_insertion" in signature.parameters:
                    model_validate = partial(method, for_insertion=False)
                else:
                    model_validate = method

                return DAOResponse(
                    success=True,
                    data=created_item
                    if isinstance(created_item, DAOResponse)
                    else model_validate(created_item),
                )
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)

    def add_update_route(self):
        @self.router.put("/{id}")
        async def update(
            id: Union[UUID, str],
            item: self.update_schema,
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            try:
                # Query the database for the item
                db_item = await self.dao.query(
                    db_session, filters={f"{self.dao.primary_key}": id}, single=True
                )

                # If item is not found, raise a 404 error
                if not db_item:
                    raise HTTPException(status_code=404, detail="Item not found")

                print(f"db_item: {db_item}")
                print(f"item: {item}")
                # Perform the update operation
                updated_item = await self.dao.update(
                    db_session=db_session, db_obj=db_item, obj_in=item
                )

                # Determine how to call model_validate
                method = getattr(self.update_schema, "model_validate")
                signature = inspect.signature(method)

                if "for_insertion" in signature.parameters:
                    model_validate = partial(method, for_insertion=False)
                else:
                    model_validate = method

                return DAOResponse(
                    success=True,
                    data=updated_item
                    if isinstance(updated_item, DAOResponse)
                    else model_validate(updated_item),
                )

            # Handle item not found in the database
            except HTTPException as e:
                # Ensure correct status code is returned
                if e.status_code == 404:
                    raise e
                else:
                    raise HTTPException(status_code=400, detail=str(e))

            # Handle database integrity errors (e.g., constraint violations)
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400, detail=f"Database integrity error: {str(e)}"
                )

            # Catch other exceptions and raise a custom exception
            except Exception as e:
                raise CustomException(f"Error updating data: {str(e)}")

    def add_delete_route(self):
        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete(
            id: Union[UUID, str], db_session: AsyncSession = Depends(get_db)
        ):
            try:
                db_item = await self.dao.get(db_session, id)
                await self.dao.delete(db_session=db_session, db_obj=db_item)
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(str(e))
