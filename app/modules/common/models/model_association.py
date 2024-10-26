import enum
from sqlalchemy.future import select
from typing import Dict, Any, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    Enum,
    inspect,
    and_,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model_base import BaseModel


class AssociationProcessor:
    def __init__(self, parent: "BaseModel", get_child_config: callable):
        self._parent = parent
        self._is_processing = False
        self._get_child_config = get_child_config

    async def process_item(
        self, item: Union["BaseModel", Dict[str, Any]], session: AsyncSession
    ):
        """Process the item and handle association logic."""
        config: Dict[str, Dict[str, Any]] = self._get_child_config(item)
        association_class: "BaseModel" = config.get("association_class", None)
        association_exclude_fields = ["created_at", "updated_at", "entity_type"]

        if not self._parent or not association_class:
            return item

        try:
            self._is_processing = True
            association_data = self._build_association_data(item, config)

            # check if association already exists
            existing_association = await self._get_existing_association(
                session,
                association_class,
                association_data,
                association_exclude_fields,
            )

            if existing_association:
                # convert model enums
                self._convert_model_enums(existing_association)

                # update the existing association
                await self._update_existing_association(
                    session,
                    existing_association,
                    association_data,
                    association_exclude_fields,
                )
            else:
                # create new association if not exists
                await self._create_new_association(
                    session, association_class, association_data
                )

            return item
        except Exception as e:
            raise Exception(f"Error processing item: {str(e)}")
        finally:
            self._is_processing = False

    def _build_association_data(self, item, config: Dict[str, Dict[str, Any]]):
        """Builds the association data using parent and item attributes."""
        association_data = {}
        entity_param_key = config.get("entity_param_key")

        # extract additional attributes from parent
        item_params_attr = config.get("item_params_attr", {})
        entity_params_attr = config.get("entity_params_attr", {})
        additional_params = getattr(item, "_entity_params", {}).get(
            entity_param_key, {}
        )

        # process parent fields (entity_id_attr)
        for parent_attr, parent_field in entity_params_attr.items():
            # if hasattr(self._parent, parent_field):
            if parent_field in self._parent.__dict__:
                association_data[parent_attr] = getattr(self._parent, parent_field)

            if parent_attr == "entity_type":
                association_data[parent_attr] = parent_field

        # process child fields (item_id_attr)
        for child_attr, child_field in item_params_attr.items():
            if hasattr(item, child_field):
                association_data[child_attr] = getattr(item, child_field)

        # merge additional params
        association_data.update(additional_params)

        return association_data

    async def _get_existing_association(
        self,
        session: AsyncSession,
        association_class: "BaseModel",
        association_data: Dict[str, Any],
        exclude_fields: Union[List[str]] = [],
    ):
        """Check if the association already exists based on foreign keys."""
        foreign_keys = self._get_foreign_keys(association_class)

        # build filter conditions based on foreign keys
        filter_conditions = [
            getattr(association_class, k) == v
            for k, v in association_data.items()
            if k in foreign_keys and k not in exclude_fields
        ]
        query = select(association_class).filter(and_(*filter_conditions))
        result = await session.execute(query)

        return result.scalars().first()

    def _get_foreign_keys(self, association_class: "BaseModel"):
        """Retrieve the foreign key columns of the association class."""
        foreign_keys = [
            fk_column.name
            for fk_column in inspect(association_class).columns
            if len(fk_column.foreign_keys) > 0
        ]

        # check if 'entity_id' and 'entity_type' should be included
        if "entity_id" in association_class.__table__.columns:
            foreign_keys.append("entity_id")

        if "entity_type" in association_class.__table__.columns:
            foreign_keys.append("entity_type")

        return foreign_keys

    def _convert_model_enums(self, existing_association: "BaseModel"):
        """Convert enum types on model to internal string representation"""
        for key in existing_association.__dict__.keys():
            field_column = getattr(existing_association, key, None)

            if isinstance(field_column, enum.Enum) or isinstance(field_column, Enum):
                setattr(existing_association, key, str(field_column.name))

    async def _update_existing_association(
        self,
        session: AsyncSession,
        existing_association: "BaseModel",
        association_data: Dict[str, Any],
        exclude_fields: Union[List[str]] = [],
    ):
        """Update fields of an existing association."""
        try:
            for key, value in association_data.items():
                if key not in exclude_fields and hasattr(existing_association, key):
                    if isinstance(value, enum.Enum):
                        setattr(existing_association, key, str(value.name))
                    elif isinstance(value, bool):
                        setattr(existing_association, key, bool(value))
                    else:
                        setattr(existing_association, key, str(value))

            session.add(existing_association)
            await session.commit()
            await session.refresh(existing_association)
            await session.flush()
        except Exception as e:
            raise Exception(f"Error updating existing association: {str(e)}")

    async def _create_new_association(
        self,
        session: AsyncSession,
        association_class: "BaseModel",
        association_data: Dict[str, Any],
    ):
        """Create a new association if one doesn't exist."""
        try:
            entity_association_data = association_class(**association_data)
            session.add(entity_association_data)
            await session.commit()
            await session.refresh(entity_association_data)
            await session.flush()
        except Exception as e:
            raise Exception(f"Error creating new association: {str(e)}")
