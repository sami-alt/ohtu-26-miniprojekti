from dataclasses import dataclass

@dataclass
class ReferenceType():
    name: str
    required_fields: list[str]
    optional_fields: list[str]
