from typing import Any, Dict, Type, TypeVar, Generic, Optional
from pydantic import BaseModel, ConfigDict, ValidationError, model_serializer
from importlib import import_module


T = TypeVar("T")


class DAOResponse(BaseModel, Generic[T]):
    success: bool = False
    error: Optional[str] = None
    data: Optional[T | Any] = None
    meta: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __init__(
        self,
        *,
        success: bool,
        data: Optional[T] = None,
        error: Optional[str] = None,
        validation_error: Optional[ValidationError] = None,
        meta: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(success=success, data=data, error=error, **kwargs)

        self.data = self._convert_data(data)
        self.error = "" if error is None else error
        self.meta = meta

        if validation_error:
            self.set_validation_errors(validation_error)

    def resolve_pydantic_schema(self, sa_instance: Any) -> Type[BaseModel]:
        """Dynamically resolve the Pydantic schema for a SQLAlchemy model instance."""
        response_mapping_cache: Dict[Type[Any], Type[BaseModel]] = {}
        sa_class = type(sa_instance)

        # Check if we already resolved this type
        if sa_class in response_mapping_cache:
            return response_mapping_cache[sa_class]

        # Derive the schema name and module path based on the model name
        sa_module_name = sa_class.__module__.replace(".models.", ".schema.")
        sa_class_name = sa_class.__name__
        schema_class_name = (
            f"{sa_class_name}Response"  # Deriving schema name conventionally
        )

        if not sa_module_name.endswith("_schema"):
            sa_module_name += "_schema"  # Adding "_schema" to the module name

        try:
            print(f"Trying to import: {sa_module_name}.{schema_class_name}")
            schema_module = import_module(sa_module_name)
            schema_class = getattr(schema_module, schema_class_name)
            response_mapping_cache[sa_class] = schema_class
            return schema_class
        except (ImportError, AttributeError) as e:
            print(f"Could not resolve Pydantic schema for {sa_class}: {e}")
            return None

    def _convert_data(self, data: Any) -> Any:
        """Convert the data to the appropriate response object based on its type."""
        if not data:
            return data

        # Determine if the data is a list or a single instance
        sa_instance = data[0] if isinstance(data, list) else data

        # Dynamically resolve the Pydantic schema
        response_class = self.resolve_pydantic_schema(sa_instance)
        print(f"response_class {response_class} {type(response_class)}")

        if not response_class:
            return data  # Fallback if no schema can be resolved

        return (
            [response_class.model_validate(item) for item in data]
            if isinstance(data, list)
            else response_class.model_validate(data)
        )

    def set_validation_errors(self, validation_error: ValidationError):
        error_messages = []
        for error in validation_error.errors():
            field = error["loc"][0]
            message = error["msg"]
            error_messages.append(f"{field} validation is incorrect: {message}")
        self.error = "; ".join(error_messages)

    def set_meta(self, meta):
        self.meta = meta

    @model_serializer(when_used="json")
    def dump_model(self) -> Dict[str, Any]:
        result = super().model_dump()

        if not self.meta:
            result.pop("meta", None)
        elif hasattr(self.meta, "total") and getattr(self.meta, "total") == 0:
            result.pop("meta", None)

        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "error": self.error,
            "data": self.data if self.data else None,
            "meta": self.meta if self.meta else None,
        }

    @classmethod
    def from_orm(cls: Type[T], obj: Any) -> T:
        return cls.model_validate(obj)

    @classmethod
    def model_validate(cls: Type[T], obj: Any) -> T:
        return cls.model_validate(obj)
