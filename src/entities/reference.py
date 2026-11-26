import re
from dataclasses import dataclass

# Characters that break .bib file unless escaped. Braces + backslashes
# left alone in case user wants to use LaTeX like {NASA} or {\"o}.
LATEX_SPECIAL = re.compile(r"(?<!\\)([&%$#_])")

def escape_latex(value: str) -> str:
    return LATEX_SPECIAL.sub(r"\\\1", value)


@dataclass
class Reference:
    type: str
    citation_key: str
    fields: dict[str, str]

    def __str__(self):
        fields_str = ", ".join((f"{name} = {{{value}}}" for name, value in self.fields.items()))
        if fields_str:
            return f"@{self.type}{{{self.citation_key}, {fields_str}}}"
        return f"@{self.type}{{{self.citation_key}}}"

    def to_bibtex(self) -> str:
        """Multi-line BibTeX entry. Empty fields are left out."""
        lines = [f"@{self.type}{{{self.citation_key},"]
        lines += [f"  {name} = {{{escape_latex(value)}}},"
                  for name, value in self.fields.items() if value]
        lines.append("}")
        return "\n".join(lines)
