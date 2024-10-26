from app.db.dbDeclarative import Base
from sqlalchemy import Column, inspect, event
from typing import Any, Dict, Type, Union, Tuple
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute, mapper


class RelationshipConfigRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RelationshipConfigRegistry, cls).__new__(cls)
            cls._instance.configs = {}
            cls._instance.table_model_cache = {
                model.__table__.fullname: model
                for model in Base.registry._class_registry.values()
                if hasattr(model, "__table__")
            }

            # update the registry
            event.listen(
                mapper,
                "mapper_configured",
                lambda *args, **kw: RelationshipConfigRegistry.__base_mapper_listener,
            )

        return cls._instance

    def __base_mapper_listener(self, mapper, class_):
        if hasattr(class_, "__table__"):
            self.table_model_cache[class_.__table__.fullname] = class_

    def _find_models_by_table_name(self, table_name):
        if table_name not in self.table_model_cache:
            self.table_model_cache = {
                model.__table__.fullname: model
                for model in Base.registry._class_registry.values()
                if hasattr(model, "__table__")
            }

        return self.table_model_cache[table_name]

    def _generate_relationship_config(
        self, model_class: Type[DeclarativeMeta]
    ) -> Dict[str, Dict[str, Any]]:
        """Generates a relationship configuration dictionary for a given SQLAlchemy model class."""
        insp = inspect(model_class)
        relationships = insp.relationships
        config: Dict[str, Dict[str, Any]] = {}

        for name, rel in relationships.items():
            entity_rel_name = ""
            entity_params_attr, item_params_attr = {}, {}

            if rel.secondary is not None:
                entity_rel_name = self._find_models_by_table_name(rel.secondary.name)

                # Generate entity and item parameter attributes
                (
                    entity_params_attr,
                    item_params_attr,
                ) = self._generate_entity_item_params(model_class, entity_rel_name)
            elif rel.remote_side is not None:
                rel_list = list(rel.remote_side)
                entity_rel_name = self._find_models_by_table_name(
                    rel_list[0].table.name
                )

                # Generate entity and item parameter attributes
                (
                    entity_params_attr,
                    item_params_attr,
                ) = self._generate_entity_item_params(model_class, entity_rel_name)

            config[name] = {
                "association_class": entity_rel_name,
                "entity_param_key": name,
                "entity_params_attr": entity_params_attr,
                "item_params_attr": item_params_attr,
            }

        return config

    def _generate_entity_item_params(
        self, model_class: Type[DeclarativeMeta], entity_rel_name: Type[DeclarativeMeta]
    ) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Generate entity_params_attr and item_params_attr for the relationship."""
        item_params_attr = {}
        entity_params_attr = {}

        for field_name, field_obj in entity_rel_name.__dict__.items():
            if isinstance(field_obj, InstrumentedAttribute) and hasattr(
                field_obj.property, "columns"
            ):
                column = field_obj.property.columns[0]

                # Handle foreign key fields
                self._handle_foreign_key_fields(
                    field_name,
                    column,
                    model_class,
                    entity_params_attr,
                    item_params_attr,
                )

                # Check for entity_type and entity_id fields
                self._handle_entity_fields(
                    field_name,
                    field_obj,
                    model_class,
                    entity_rel_name,
                    entity_params_attr,
                )

                # Handle other non-foreign key fields
                self._handle_non_foreign_key_fields(
                    field_name, column, item_params_attr
                )

        return entity_params_attr, item_params_attr

    def _handle_foreign_key_fields(
        self,
        field_name: str,
        column: Column,
        model_class: Type[DeclarativeMeta],
        entity_params_attr: Dict[str, str],
        item_params_attr: Dict[str, str],
    ):
        """Handle foreign key fields by populating entity_params_attr and item_params_attr."""
        if column.foreign_keys:
            for fk in column.foreign_keys:
                if fk.column.table == model_class.__table__:
                    entity_params_attr[field_name] = fk.column.name
                else:
                    item_params_attr[field_name] = fk.column.name

    # TODO: Add check to determine if relationship primaryjoin or secondary
    # join has certain conditions on the entity_id or entity_type fields
    def _handle_entity_fields(
        self,
        field_name: str,
        field_obj: InstrumentedAttribute,
        model_class: Type[DeclarativeMeta],
        entity_rel_name: Type[DeclarativeMeta],
        entity_params_attr: Dict[str, str],
    ):
        """Check for and handle entity_type and entity_id fields."""
        if field_name == "entity_type" and "entity_id" in entity_rel_name.__dict__:
            enum_class = field_obj.property.columns[0].type.enums

            if (
                model_class.__tablename__.lower() in enum_class
                or model_class.__name__.lower() in enum_class
            ):
                entity_params_attr["entity_id"] = (
                    model_class.__table__.primary_key.columns[0].name
                )
                entity_params_attr["entity_type"] = (
                    model_class.__tablename__.lower()
                    if model_class.__tablename__.lower() in enum_class
                    else model_class.__name__.lower()
                )

    def _handle_non_foreign_key_fields(
        self, field_name: str, column: Column, item_params_attr: Dict[str, str]
    ):
        """Handle non-foreign key fields and populate item_params_attr."""
        if not column.foreign_keys and field_name != "entity_id":
            # and entity_rel_name.__tablename__.lower() not in field_name
            item_params_attr[field_name] = field_name

    def get_config(
        self,
    ) -> Dict[str, Union[Dict[str, Union[Any | Dict[str, Any]]], Any]]:
        """Returns the current complete configuration."""
        return self.configs

    def register_model(
        self, model_class: Type[DeclarativeMeta], register_action="default_action"
    ):
        """Registers a model and updates its relationship configuration in the registry."""

        # print(f"self.configs.keys(): {model_class.__name__.lower()} || {self.configs.keys()}")
        if model_class.__tablename__.lower() not in self.configs.keys():
            print(f"\nRegistering {model_class.__name__.lower()}")
            config = self._generate_relationship_config(model_class)
            self.configs[model_class.__tablename__.lower()] = config
            print(f"Done with Registration {model_class.__tablename__.lower()}!")
        else:
            print(f"Already Registered {model_class.__tablename__.lower()}!")


# create model registry
registry = RelationshipConfigRegistry()
