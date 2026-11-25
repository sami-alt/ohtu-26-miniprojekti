import os
import tomllib

from entities.reference_type import ReferenceType

toml_path = os.path.join(os.path.dirname(__file__), "types.toml")
with open(toml_path, "rb") as f:
    data = tomllib.load(f)

type_dict = {
    type_name: ReferenceType(type_name, type_data["required"], type_data["optional"])
    for type_name, type_data in data.items()
}

def get_reference_type(name: str) -> ReferenceType | None:
    """Get a named reference type from the repository."""
    return type_dict.get(name)

def get_reference_types() -> list[ReferenceType]:
    """Get all reference types from the repository."""
    return list(type_dict.values())
