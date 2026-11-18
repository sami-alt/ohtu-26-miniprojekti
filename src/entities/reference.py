from dataclasses import dataclass

@dataclass
class Reference:
    type: str
    citation_key: str
    fields: dict[str, str]

    def __str__(self):
        fields_str = ", ".join((f"{name} = {{{value}}}" for name, value in self.fields.items()))
        if fields_str:
            return f"@{self.type}{{{self.citation_key}, {fields_str}}}"
        else:
            return f"@{self.type}{{{self.citation_key}}}"

