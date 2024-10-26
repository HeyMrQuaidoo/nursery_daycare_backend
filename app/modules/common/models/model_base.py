import pytz
from datetime import datetime
from functools import lru_cache
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from typing import Dict, List, Any, Optional, Tuple, Union
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    Session,
)
from sqlalchemy import (
    DateTime,
    UUID,
    MetaData,
    Table,
    inspect,
    exists,
    event,
)

from app.db.dbDeclarative import Base
from app.modules.common.models.model_registry import registry
from app.modules.common.models.model_base_collection import BaseModelCollection


class BaseModel(Base, AsyncAttrs):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.utc),
        onupdate=lambda: datetime.now(pytz.utc),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entity_params: Dict[str, Any] = {}
        self._set_collection_parents()

    @staticmethod
    def setup_model_dynamic_listener(table_name: str, model_class):
        metadata: MetaData = Base.metadata
        table = metadata.tables.get(table_name.lower())

        if not isinstance(table, Table):
            raise ValueError(f"Table {table_name} not found in metadata.")

        # on model create
        event.listen(
            table,
            "after_create",
            lambda target, connection, **kw: registry.register_model(
                model_class, "after_create"
            ),
        )

        # on model load
        event.listen(
            model_class,
            "load",
            lambda target, connection, **kw: registry.register_model(
                model_class, "load"
            ),
        )

        # on model insert
        event.listen(
            model_class,
            "before_insert",
            lambda *arg: registry.register_model(model_class, "before_insert"),
            propagate=True,
        )

    def _set_collection_parents(self):
        """dynamically set the parent for all relationships that are instances of BaseModelCollection."""
        mapper = inspect(self.__class__)

        for relationship in mapper.relationships:
            attr_name = relationship.key
            attr_value = getattr(self, attr_name, None)

            if isinstance(attr_value, BaseModelCollection):
                attr_value.set_parent(self)

    def set_entity_params(self, entity_data: Dict[str, Any]):
        """
        Set extra entity parameters, merging the entity_data dictionary into _entity_params.

        :param entity_data: A dictionary containing entity data, with arbitrary keys and values.
        """
        if not hasattr(self, "_entity_params"):
            setattr(self, "_entity_params", {})

        self._entity_params = self._merge_dicts(self._entity_params, entity_data)

    def get_entity_params(self) -> Dict[str, Any]:
        return self._entity_params

    def get_entity_type(self):
        return str(self.__tablename__)

    def execute_select(self, stmt: str):
        from app.db.dbManager import DBManager

        db_manager = DBManager()

        session: Session = db_manager.db_module.get_sync_db()
        return session.execute(stmt)

    @lru_cache(maxsize=1024)
    def _cached_entity_exists(
        self, table_name: str, column_name: str, entity_id: Any
    ) -> bool:
        try:
            table_class = Base.metadata.tables.get(table_name.lower())

            if not isinstance(table_class, Table):
                raise ValueError(f"Model class for {table_name} not found")

            stmt = select(exists().where(table_class.c[column_name] == str(entity_id)))
            result = self.execute_select(stmt)

            return result.scalar()
        except Exception as e:
            raise RuntimeError(f"Error checking if entity exists: {e}")

    def validate_entity(
        self,
        entity_id: Any,
        entity_type: Optional[Union[str, UUID]],
        entity_map: Optional[Dict[str, Tuple[str, str]]],
    ) -> Any:
        table_name, column_name = entity_map.get(entity_type, (None, None))

        if not table_name or not column_name:
            raise ValueError(f"Invalid entity type: {entity_type}")

        if not self._cached_entity_exists(table_name, column_name, entity_id):
            raise ValueError(f"Invalid {str(entity_type)} ID: {entity_id}")

        return entity_id

    def _merge_dicts(
        self, source: Dict[str, Any], updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recursively merge two dictionaries. If the same key exists, the values in 'updates' take precedence."""

        for key, value in updates.items():
            if (
                isinstance(value, dict)
                and key in source
                and isinstance(source.get(key), dict)
            ):
                source[key] = self._merge_dicts(source[key], value)
            else:
                source[key] = value
        return source

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        return {
            key: (str(value) if isinstance(value, (datetime, UUID)) else value)
            for key, value in self.__dict__.items()
            if not key.startswith("_") and key not in exclude
        }

    def model_dump(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        return {
            key: (str(value) if isinstance(value, (datetime, UUID)) else value)
            for key, value in self.__dict__.items()
            if not key.startswith("_") and key not in exclude
        }
