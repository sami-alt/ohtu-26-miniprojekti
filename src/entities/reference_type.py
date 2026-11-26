from dataclasses import dataclass

@dataclass
class ReferenceType():
    name: str
    required_fields: list[str]
    optional_fields: list[str]
    display_name: str | None = None

    @property
    def fields(self) -> list[str]:
        return self.required_fields + self.optional_fields

    def get_display_name(self) -> str:
        """Return the display name if it exists, else return regular name."""
        return self.display_name or self.name
