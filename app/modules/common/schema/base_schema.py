from faker import Faker
from datetime import date
from sqlalchemy import inspect
from typing import List, Optional, Type, Dict
from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel, ConfigDict, create_model

BaseFaker = Faker()
SchemasDictType = Dict[str, Type[BaseModel]]


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
    )


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, use_enum_values=True
    )

    @classmethod
    def generate_schemas_for_sqlalchemy_model(
        cls, model: Type[DeclarativeMeta], excludes: List[str] = ["id"]
    ) -> Dict[str, Type[BaseModel]]:
        """
        Generates Pydantic schemas for a given SQLAlchemy model.
        Returns a dictionary with 'model_schema', 'create_schema', and 'update_schema'.
        """
        columns = {c.name: (c.type.python_type, ...) for c in inspect(model).c}
        primary_keys = [key.name for key in inspect(model).primary_key]

        default_excludes: List[str] = ["created_at", "updated_at"]

        model_schema = create_model(
            f"{model.__name__}ModelSchema",
            **{
                name: (Optional[typ], None)
                for name, (typ, _) in columns.items()
                if name not in default_excludes
            },
            __config__=ConfigDict(from_attributes=True),
        )

        default_excludes.extend(excludes)

        create_schema = create_model(
            f"{model.__name__}CreateSchema",
            **{
                name: (Optional[typ], None)
                for name, (typ, _) in columns.items()
                if name not in default_excludes
            },
            __config__=ConfigDict(from_attributes=True),
        )

        update_schema = create_model(
            f"{model.__name__}UpdateSchema",
            **{
                name: (Optional[typ], None)
                for name, (typ, _) in columns.items()
                if name not in default_excludes
            },
            __config__=ConfigDict(from_attributes=True),
        )

        return {
            "model_schema": model_schema,
            "create_schema": create_schema,
            "update_schema": update_schema,
            "primary_keys": primary_keys,
        }
