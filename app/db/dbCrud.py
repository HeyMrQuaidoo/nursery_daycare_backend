from uuid import UUID
from importlib import import_module
from sqlalchemy.future import select
from sqlalchemy import and_, between, func, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.orm import selectinload, InstrumentedAttribute
from typing import List, Type, TypeVar, Dict, Any, Union, Optional

# core
from app.core.errors import (
    IntegrityError,
    RecordNotFoundException,
    ForeignKeyError,
    UniqueViolationError,
)

# enums
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# models
from app.modules.common.models.model_base import (
    BaseModelCollection,
    BaseModel,
    registry,
)

DBModelType = TypeVar("DBModelType")


class BaseMixin:
    primary_key: str

    def __init__(
        self,
        model: Type[DBModelType],
        detail_mappings: Optional[Dict[str, Any]],
        model_entity_params: Optional[Dict[str, Dict[str, Any]]],
        excludes: Optional[List[str]] = None,
        *args,
        **kwargs,
    ):
        self.model = model
        self.excludes = excludes if excludes is not None else []
        self.detail_mappings = detail_mappings
        self.model_entity_params = model_entity_params
        self.args = args
        self.kwargs = kwargs
        self.primary_key = kwargs.get("primary_key")

    def get_model_fields(self) -> List[str]:
        mapper = inspect(self.model)
        return [column.key for column in mapper.attrs if hasattr(column, "columns")]

    def get_entity_type(self, db_obj: DBModelType) -> EntityTypeEnum:
        if isinstance(
            db_obj, getattr(import_module("app.modules.auth.models.user"), "User")
        ):
            return EntityTypeEnum.user
        if isinstance(
            db_obj, getattr(import_module("app.modules.auth.models.role"), "Role")
        ):
            return EntityTypeEnum.role
        elif isinstance(
            db_obj,
            getattr(
                import_module("app.modules.properties.models.property"), "Property"
            ),
        ):
            return EntityTypeEnum.property
        elif isinstance(
            db_obj,
            getattr(
                import_module("app.modules.properties.models.rental_history"),
                "PastRentalHistory",
            ),
        ):
            return EntityTypeEnum.pastrentalhistory
        elif isinstance(
            db_obj,
            getattr(import_module("app.modules.billing.models.account"), "Account"),
        ):
            return EntityTypeEnum.account
        else:
            raise ValueError(f"Unknown entity type for object {db_obj}")

    def filter_input_fields(
        self, obj_in: Union[Dict[str, Any] | PydanticBaseModel | Any]
    ) -> Dict[str, Any]:
        try:
            if isinstance(obj_in, PydanticBaseModel) or isinstance(obj_in, self.model):
                obj_in = obj_in.model_dump()
            elif not isinstance(obj_in, dict):
                raise ValueError("Input must be a dictionary or a BaseModel instance.")

            valid_fields = self.get_model_fields()

            return {
                k: v for k, v in obj_in.items() if k in valid_fields and v is not None
            }
        except Exception as e:
            raise Exception(e)

    def validate_primary_key(
        self, uuid_to_test: Union[str, UUID], version: int = 4
    ) -> Union[str, UUID]:
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return str(uuid_to_test)

        return uuid_obj

    async def commit_and_refresh(
        self, db_session: AsyncSession, obj: DBModelType
    ) -> DBModelType:
        try:
            await db_session.commit()
            await db_session.refresh(obj)
            return obj

        except ForeignKeyError as e:
            await db_session.rollback()
            raise ForeignKeyError(f"Foreign key violation: {str(e)}")
        except Exception as e:
            await db_session.rollback()
            raise Exception(f"Error committing data: {str(e)}")

    def update_none_values_with_parent(
        self, detail_obj_list, entity_parent_params_attr: dict, parent_obj: dict
    ):
        """
        Updates items in detail_obj_list by setting fields with None values
        to their corresponding parent values using entity_parent_params_attr.

        Args:
            detail_obj_list (list): List of detail objects (dictionaries) to update.
            entity_parent_params_attr (dict): A mapping of keys from detail_obj to keys in the parent object.
            parent_obj (dict): The parent object containing values for the linked keys.
        """
        for item in detail_obj_list:
            # Find keys with None values in the item
            keys_with_none = [key for key, value in item.items() if value is None]

            if keys_with_none:
                print(f"\tFound keys with None: {keys_with_none}")

                # For each key with None, check if there is a corresponding parent key
                for key in keys_with_none:
                    # Get the corresponding linked key in entity_parent_params_attr
                    parent_key = entity_parent_params_attr.get(key)

                    if parent_key:
                        # Set the current item's key to the parent value using the linked key
                        parent_value = parent_obj.get(parent_key)

                        if parent_value is not None:
                            item[key] = parent_value
                            print(
                                f"\tSetting {key} in item to parent value: {parent_value}"
                            )
                        else:
                            print(
                                f"\tParent value for {parent_key} is None, skipping setting {key}"
                            )
                    else:
                        print(
                            f"\tNo parent key found for {key} in entity_parent_params_attr"
                        )
            else:
                print(f"\n\tNo need to update none values with parent values")

    async def create_or_update_relationships(
        self,
        db_session: AsyncSession,
        db_obj: Union[DBModelType, BaseModel],
        obj_data: Union[Dict[str, Any], PydanticBaseModel],
    ):
        try:
            # Get config registry
            config = registry.get_config()

            # Get object config
            obj_config = config.get(db_obj.__tablename__.lower(), {})
            if not config or not obj_config:
                raise ValueError("Issue trying to determine db_obj config mapping")

            print(f"Inspect Detail Mapping: {self.detail_mappings}")
            for mapped_obj_key, mapped_obj_dao in self.detail_mappings.items():
                # Get the list of objects to check from obj_data
                detail_obj_list = obj_data.get(mapped_obj_key, [])
                if not detail_obj_list:
                    print(f"\n\tSkipped {mapped_obj_key}")
                    continue

                print(f"\n\tChecking detail mapping key for objects: {mapped_obj_key}")
                print(f"\tChecking detail objects list: {detail_obj_list}")

                # Get parent object data for updating None values
                parent_obj = db_obj.model_dump()
                if not parent_obj:
                    continue

                # Retrieve entity attributes and params
                entity_child_attrs = obj_config.get(mapped_obj_key.lower(), {})
                if not entity_child_attrs:
                    continue
                print(f"\t\tInspect Child Entity attributes on Parent object {entity_child_attrs}")

                entity_parent_params_attr = entity_child_attrs.get("entity_params_attr")
                print(f"\t\t\tInspect Child Entity Parent Params {entity_parent_params_attr}")
                if isinstance(detail_obj_list, list):
                    self.update_none_values_with_parent(
                        detail_obj_list, entity_parent_params_attr, parent_obj
                    )

                # Initialize variables and process items in detail_obj_list
                new_items = []
                model_attr = getattr(db_obj, mapped_obj_key, None)

                print(f"\n\tDetermine any already linked relationship items from DB {model_attr}")
                for detail_obj in detail_obj_list:
                    if detail_obj is None:
                        continue  # Skip if detail_obj is None

                    print(f"\n\t\tAbout to create a new mapped object item for model: {self.model.__name__}")
                    mapped_obj_created_item = await mapped_obj_dao.create_or_update(
                        db_session=db_session, obj_in=detail_obj
                    )
                    print(f"\t\tDone creating mapped object item for model {self.model.__name__}")

                    # Single flush and refresh after each item
                    await db_session.flush()
                    mapped_obj_created_item = await self.commit_and_refresh(
                        db_session=db_session, obj=mapped_obj_created_item
                    )

                    # Entity config parameters
                    if isinstance(mapped_obj_created_item, BaseModel):
                        entity_config = obj_config or config.get(self.model.__name__.lower(), {})
                        entity_param_keys = (
                            entity_config.get(mapped_obj_key.lower(), {})
                            .get("item_params_attr", {})
                            .keys()
                        )
                        print(f"\t\t\tInspect Child Entity Item Params {entity_param_keys}")
                        if entity_param_keys:
                            filtered_params = {
                                key: detail_obj[key]
                                for key in entity_param_keys
                                if key in detail_obj and detail_obj[key] is not None
                            }
                            if filtered_params:
                                mapped_obj_created_item.set_entity_params(
                                    {mapped_obj_key: filtered_params}
                                )
                        print(f"\t\t\tFiltered Child Entity Item Params {filtered_params}")

                    # Add to new items
                    new_items.append(mapped_obj_created_item)
                    print(f"\t\t\tNew Items Are: {new_items}")

                # Batch add items to the collection
                if model_attr is not None and isinstance(model_attr, list):
                    if isinstance(model_attr, BaseModelCollection):
                        model_attr = (
                            model_attr.set_parent(db_obj)
                            if not model_attr._parent
                            else model_attr
                        )
                        print(f"\t\tModel is BaseModelCollection {isinstance(model_attr, BaseModelCollection)}")

                        for item in new_items:
                            if hasattr(item, "_sa_instance_state"):
                                print(f"\n\t\tModel is _sa_instance_state {hasattr(item, '_sa_instance_state')}")
                                print(f"\t\tAbout to append BaseModelCollection item {item}")
                                item = await model_attr.append_item(item, db_session)
                                print(f"\t\tDone appending BaseModelCollection item {item}")
                            else:
                                raise ValueError(f"Item {item} is not a valid ORM instance")
                    else:
                        model_attr.extend(new_items)
                else:
                    if all(hasattr(item, "_sa_instance_state") for item in new_items):
                        new_collection = (
                            BaseModelCollection(new_items, parent=db_obj)
                            if isinstance(model_attr, BaseModelCollection)
                            else new_items
                        )
                        if isinstance(new_collection, list):
                            for item in new_collection:
                                setattr(db_obj, mapped_obj_key, item)
                        else:
                            setattr(db_obj, mapped_obj_key, new_collection)
                    else:
                        raise ValueError("Not all items are valid ORM instances")

                # Single flush and refresh after each mapping
                await db_session.flush()
                await db_session.refresh(db_obj)
                db_obj = await self.commit_and_refresh(
                    db_session=db_session, obj=db_obj
                )

        except Exception as e:
            raise Exception(f"Error in create_or_update_relationships: {str(e)}")

    async def create_or_update_relationships_old(
        self,
        db_session: AsyncSession,
        db_obj: Union[DBModelType, BaseModel],
        obj_data: Union[Dict[str, Any], PydanticBaseModel],
    ):
        try:
            # get config registry
            config = registry.get_config()

            # get object config
            obj_config = config.get(db_obj.__tablename__.lower(), {})

            if not config or not obj_config:
                raise ValueError(
                    f"Issue trying to determine db_obj config mapping"
                )
            
            print(f"Inspect Detail Mapping: {self.detail_mappings}")
            for mapped_obj_key, mapped_obj_dao in self.detail_mappings.items():

                # Get the list of objects to check from obj_data
                detail_obj_list = obj_data.get(mapped_obj_key, [])

                # Safeguard against None values in the obj_data
                if not detail_obj_list:
                    print(f"\n\tSkipped {mapped_obj_key}")
                    continue

                print(f"\n\tChecking detail mapping key for objects: {mapped_obj_key}")
                print(f"\tChecking detail objects list: {detail_obj_list}")

                # Find entity parent params
                parent_obj = db_obj.model_dump()

                # skip if parent_obj is None
                if not parent_obj:
                    continue

                entity_child_attrs = obj_config.get(
                    mapped_obj_key.lower(), {}
                )
                print(f"\t\tInspect Child Entity attributes on Parent object {entity_child_attrs}")

                # skip if entity_child_attrs is None or empty
                if not entity_child_attrs:
                    continue

                entity_parent_params_attr = entity_child_attrs.get("entity_params_attr")
                print(f"\t\t\tInspect Child Entity Parent Params {entity_parent_params_attr}")

                # Call the helper method to update the None values
                if isinstance(detail_obj_list, list):
                    self.update_none_values_with_parent(
                        detail_obj_list, entity_parent_params_attr, parent_obj
                    )

                mapped_obj_dao: DBOperations = mapped_obj_dao
                print(f"\tDetermining Mapped object DAO for model {mapped_obj_dao} {self.model.__name__}")

                if not isinstance(detail_obj_list, list):
                    detail_obj_list = [detail_obj_list]

                new_items = []
                model_attr = getattr(db_obj, mapped_obj_key, None)
                print(f"\n\tDetermine any already linked relationship items from DB {model_attr}")

                for detail_obj in detail_obj_list:
                    if detail_obj is None:
                        continue  # skip if detail_obj is None
                    
                    print(f"\n\t\tAbout to create a new mapped object item for model: {self.model.__name__}")
                    mapped_obj_created_item = await mapped_obj_dao.create_or_update(
                        db_session=db_session, obj_in=detail_obj
                    )
                    print(f"\t\tDone creating mapped object item for model {self.model.__name__}")
                    
                    print(f"\t\tBefore DB Flush")
                    print(f"\t\t\tMapped object item model type {type(mapped_obj_created_item)}")
                    print(f"\t\t\tMapped object item model {mapped_obj_created_item}")
                    print(f"\t\t\tMapped object item model dict {mapped_obj_created_item.__dict__}")

                    await db_session.flush()
                    mapped_obj_created_item = await self.commit_and_refresh(
                        db_session=db_session, obj=mapped_obj_created_item
                    )
                    print(f"\t\tAfter DB commit and refresh")
                    print(f"\t\t\tMapped object item model type {type(mapped_obj_created_item)}")
                    print(f"\t\t\tMapped object item model {mapped_obj_created_item}")
                    print(f"\t\t\tMapped object item model dict {mapped_obj_created_item.__dict__}")
                    print(f"\t\t\tMapped object item model instance {isinstance(mapped_obj_created_item, BaseModel)}")

                    if isinstance(mapped_obj_created_item, BaseModel):
                        entity_config = obj_config if obj_config else config.get(self.model.__name__.lower(), {})

                        # Get keys for relationship fields
                        entity_param_keys = (
                            entity_config.get(mapped_obj_key.lower(), {})
                            .get("item_params_attr", {})
                            .keys()
                        )
                        print(f"\t\t\tInspect Child Entity Item Params {entity_param_keys}")

                        # Filter keys based on what is passed in the detail object
                        if entity_param_keys:
                            filtered_params = {
                                key: detail_obj[key]
                                for key in entity_param_keys
                                if key in detail_obj and detail_obj[key] is not None
                            }

                            if filtered_params:
                                mapped_obj_created_item.set_entity_params(
                                    {mapped_obj_key: filtered_params}
                                )
                            print(f"\t\t\tFiltered Child Entity Item Params {filtered_params}")

                    new_items.append(mapped_obj_created_item)
                    await db_session.flush()
                    await db_session.refresh(mapped_obj_created_item)
                    print(f"\t\tAfter Flush and Refresh")
                    print(f"\t\t\tMapped object item model type {type(mapped_obj_created_item)}")
                    print(f"\t\t\tMapped object item model {mapped_obj_created_item}")
                    print(f"\t\t\tMapped object item model dict {mapped_obj_created_item.__dict__}")
                    print(f"\t\t\tMapped object item model instance {isinstance(mapped_obj_created_item, BaseModel)}")
                    new_items.append(mapped_obj_created_item)
                    print(f"\t\t\tNew Items Are: {new_items}")

                # Now batch add the items to the collection
                if model_attr is not None and isinstance(model_attr, list):

                    if isinstance(model_attr, BaseModelCollection):
                        model_attr = (
                            model_attr.set_parent(db_obj)
                            if not model_attr._parent
                            else model_attr
                        )
                        print(f"\t\tModel is BaseModelCollection {isinstance(model_attr, BaseModelCollection)}")

                        for item in new_items:
                            if hasattr(item, "_sa_instance_state"):
                                print(f"\n\t\tModel is _sa_instance_state {hasattr(item, "_sa_instance_state")}")
                                print(f"\t\tAbout to append BaseModelCollection item {item}")
                                item = await model_attr.append_item(item, db_session)
                                print(f"\t\tDone appending BaseModelCollection item {item}")
                            else:
                                raise ValueError(
                                    f"Item {item} is not a valid ORM instance"
                                )
                    else:
                        model_attr.extend(new_items)
                else:
                    if all(hasattr(item, "_sa_instance_state") for item in new_items):
                        new_collection = (
                            BaseModelCollection(new_items, parent=db_obj)
                            if isinstance(model_attr, BaseModelCollection)
                            else new_items
                        )
                        if isinstance(new_collection, list):
                            for item in new_collection:
                                setattr(db_obj, mapped_obj_key, item)
                        else:
                            setattr(db_obj, mapped_obj_key, new_collection)
                    else:
                        raise ValueError("Not all items are valid ORM instances")

                await db_session.flush()
                await db_session.refresh(mapped_obj_created_item)
                db_obj = await self.commit_and_refresh(
                    db_session=db_session, obj=db_obj
                )

        except Exception as e:
            raise Exception(f"Error in create_or_update_relationships: {str(e)}")


class CreateMixin(BaseMixin):
    async def create(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any] | PydanticBaseModel | Any],
    ) -> DBModelType:
        try:
            db_obj = self.model(**self.filter_input_fields(obj_in))
            db_session.add(db_obj)
            await self.commit_and_refresh(db_session=db_session, obj=db_obj)

            obj_data = (
                obj_in.model_dump()
                if isinstance(obj_in, PydanticBaseModel)
                or isinstance(obj_in, BaseModel)
                and not isinstance(obj_in, dict)
                else obj_in
            )

            if self.detail_mappings:
                print(f"\tin self.detail_mappings {self.detail_mappings}\n")
                await self.create_or_update_relationships(db_session, db_obj, obj_data)

            await db_session.flush()
            return await self.commit_and_refresh(db_session=db_session, obj=db_obj)

        except IntegrityError as e:
            await db_session.rollback()
            raise UniqueViolationError(e)
        except Exception as e:
            await db_session.rollback()
            raise Exception(str(e))


class ReadMixin(BaseMixin):
    async def get(
        self,
        db_session: AsyncSession,
        id: Union[UUID, str, int],
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[DBModelType]:
        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = [
            selectinload(getattr(self.model, attr)) for attr in relationships
        ]

        # find model object based on primary key
        filter = {f"{self.primary_key}": self.validate_primary_key(id)}
        conditions = [getattr(self.model, k) == v for k, v in filter.items()]
        query = (
            select(self.model)
            .filter(and_(*conditions))
            .options(*query_options)
            .offset(skip)
            .limit(limit)
        )

        executed_query = await db_session.execute(query)
        result = executed_query.scalar_one_or_none()

        if not result:
            raise RecordNotFoundException(model=self.model.__name__, id=id)

        return result

    async def get_all(
        self, db_session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> List[DBModelType]:
        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = [
            selectinload(getattr(self.model, attr)) for attr in relationships
        ]

        query = select(self.model).options(*query_options).offset(offset).limit(limit)
        executed_query = await db_session.execute(query)
        result = executed_query.scalars().all()

        return result

    async def query_on_joins(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        order_by: Optional[List[InstrumentedAttribute]] = None,
        join_conditions: Optional[List] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Union[List[DBModelType], Optional[DBModelType]]:
        # separate main model filters and joined table filters
        main_model_conditions = []
        join_conditions_filters = []

        for key, value in filters.items():
            if "." in key:
                # indicates a filter on a join table
                table_name, column_name = key.split(".")
                join_conditions_filters.append((table_name, column_name, value))
            else:
                # filter on the main model
                main_model_conditions.append(getattr(self.model, key) == value)
        query = select(self.model)

        # apply joins
        if join_conditions:
            for join_condition in join_conditions:
                query = query.join(*join_condition)

        # apply main model conditions
        query = query.filter(and_(*main_model_conditions))

        # apply filters on joined tables
        for table_name, column_name, value in join_conditions_filters:
            join_model = None
            for join_condition in join_conditions:
                if join_condition[0].__name__ == table_name:
                    join_model = join_condition[0]
                    break
            if join_model:
                query = query.filter(getattr(join_model, column_name) == value)

        # apply options
        if options:
            query = query.options(*options)

        # apply ordering
        if order_by:
            query = query.order_by(*order_by)

        query_result = await db_session.execute(query.offset(skip).limit(limit))

        return (
            query_result.unique().scalar_one_or_none()
            if single
            else query_result.unique().scalars().all()
        )

    async def query(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        order_by: Optional[List[InstrumentedAttribute]] = None,
    ) -> Union[List[DBModelType], Optional[DBModelType]]:
        # conditions = [getattr(self.model, k) == v for k, v in filters.items()]
        conditions = []
        for key, value in filters.items():
            # Check if the filter value is a dictionary with "$gte" and "$lt" keys
            if isinstance(value, dict) and "$gte" in value and "$lt" in value:
                # Apply a between condition for this field
                conditions.append(
                    between(getattr(self.model, key), value["$gte"], value["$lt"])
                )
            else:
                # Apply a standard equality condition
                conditions.append(getattr(self.model, key) == value)

        query = select(self.model).filter(and_(*conditions))

        if options:
            query = query.options(*options)

        if order_by:
            query = query.order_by(*order_by)

        query_result = await db_session.execute(query)

        return (
            query_result.scalar_one_or_none()
            if single
            else query_result.scalars().all()
        )

    # async def query_count(self, db_session: AsyncSession) -> int:
    #     executed_query = await db_session.execute(
    #         select(func.count()).select_from(self.model)
    #     )
    #     count = executed_query.scalar()

    #     return count
    async def query_count(
        self, db_session: AsyncSession, filter_condition: Dict[str, Any] = None
    ) -> int:
        query = select(func.count()).select_from(self.model)

        if filter_condition:
            filters = [
                getattr(self.model, key) == value
                for key, value in filter_condition.items()
            ]
            query = query.where(and_(*filters))

        executed_query = await db_session.execute(query)
        count = executed_query.scalar()

        return count

    async def query_on_create(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single: bool = False,
        options: Optional[List[InstrumentedAttribute]] = None,
        create_if_not_exist: bool = False,
    ) -> Optional[DBModelType]:
        try:
            result = await self.query(
                db_session=db_session, filters=filters, single=single, options=options
            )

            if result:
                return result
            elif create_if_not_exist:
                db_obj = self.model(**filters)
                db_session.add(db_obj)

                return await self.commit_and_refresh(db_session=db_session, obj=db_obj)
        except Exception as e:
            raise Exception(str(e))


class UpdateMixin(BaseMixin):
    async def update(
        self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]
    ) -> DBModelType:
        try:
            obj_in_fields = self.filter_input_fields(obj_in)
            # ensure obj_in_fields is not None before iterating
            if obj_in_fields is None:
                raise ValueError("Input fields cannot be None")

            for field, value in obj_in_fields.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            db_session.add(db_obj)

            obj_data = (
                obj_in.model_dump()
                if isinstance(obj_in, PydanticBaseModel)
                or isinstance(obj_in, BaseModel)
                else obj_in
            )
            if self.detail_mappings:
                print(f"\tin update self.detail_mappings {self.detail_mappings}\n")
                await self.create_or_update_relationships(db_session, db_obj, obj_data)

            return await self.commit_and_refresh(db_session=db_session, obj=db_obj)

        except Exception as e:
            await db_session.rollback()
            raise Exception(f"Error updating data: {str(e)}")


class DeleteMixin(BaseMixin):
    async def delete(
        self, db_session: AsyncSession, db_obj: DBModelType
    ) -> DBModelType:
        await db_session.delete(db_obj)
        await db_session.commit()


class DBOperations(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(
        self,
        model: Type[DBModelType],
        detail_mappings: Optional[Dict[str, Any]] = {},
        model_entity_params: Optional[Dict[str, Any]] = {},
        excludes: Optional[List[str]] = [],
        *args,
        **kwargs,
    ):
        self.model = model
        self.excludes = excludes if excludes is not None else []
        self.detail_mappings = detail_mappings
        self.model_entity_params = model_entity_params

        super().__init__(
            self.model,
            excludes=excludes,
            detail_mappings=detail_mappings,
            model_entity_params=model_entity_params,
            *args,
            **kwargs,
        )

    async def create_or_update(
        self,
        db_session: AsyncSession,
        obj_in: Union[Dict[str, Any], DBModelType],
        filters: Optional[Dict[str, Any]] = None,
        update_existing: bool = True,
    ) -> DBModelType:
        try:
            existing_obj = None
            primary_key_value = obj_in.get(self.primary_key)
            print(f"\tcreate_or_update: {self.primary_key} :::: {primary_key_value}")

            if primary_key_value:
                try:
                    if not filters:
                        filters = {f"{self.primary_key}": str(primary_key_value)}

                    existing_obj = await self.query(
                        db_session=db_session, filters=filters, single=True
                    )
                except RecordNotFoundException:
                    existing_obj = None

            if existing_obj and update_existing:
                return await self.update(
                    db_session=db_session, db_obj=existing_obj, obj_in=obj_in
                )
            else:
                try:
                    input_for_creation = self.model(**obj_in)
                except AttributeError:
                    input_for_creation = obj_in
                except Exception:
                    # Filter out the keys from obj_in that are in self.excludes
                    input_for_creation = {
                        k: v for k, v in obj_in.items() if k not in self.excludes
                    }
                    # input_for_creation = self.model(**self.filter_input_fields(obj_in))

                return await self.create(
                    db_session=db_session, obj_in=input_for_creation
                )
        except Exception as e:
            raise Exception(str(e))
