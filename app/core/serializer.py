from pydantic import BaseModel
from typing import Any, Type, TypeVar, Dict, Optional
import json

T = TypeVar("T", bound=BaseModel)


class JSONSerializer:
    """
    Utility class for serializing Pydantic models and deserializing data from json.
    """

    @staticmethod
    def serialize(obj: Any) -> str:
        """
        Serialize a Pydantic model or other data types into a JSON string.

        If the input is a Pydantic model, it includes the model class name as metadata.
        """
        if isinstance(obj, BaseModel):
            data = obj.model_dump_json()  # Serialize Pydantic model to JSON
            return f"{obj.__class__.__name__}::{data}"  # Prefix with model name
        elif isinstance(obj, (dict, list, int, float, str, bool, type(None))):
            return json.dumps(obj)  # Serialize other common data types
        else:
            raise ValueError(f"Cannot serialize object of type {type(obj)}")

    @staticmethod
    def deserialize(
        data: str, model_registry: Optional[Dict[str, Type[BaseModel]]] = None
    ) -> Any:
        """
        Deserialize a JSON string from the json back into a Pydantic model or native Python data types.

        If the data includes a model name prefix, it uses the provided model registry to find the model class.
        """
        if "::" in data:
            # Split into model name and JSON data
            model_name, json_data = data.split("::", 1)
            if model_registry and model_name in model_registry:
                model_class = model_registry[model_name]
                return model_class.parse_raw(
                    json_data
                )  # Deserialize into Pydantic model
        return json.loads(data)  # Fallback to plain JSON deserialization
