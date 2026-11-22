from sqlalchemy import text

from config import db
from entities.reference import Reference

def get_references() -> list[Reference]:
    """Get all references from ther repository."""
    with db.session.begin():
        ref_query = text("SELECT reference_type, citation_key FROM reference_entries")

        return [Reference(
            type=row[0],
            citation_key=row[1],
            fields=_get_fields(row[1])
        ) for row in db.session.execute(ref_query).fetchall()]


def get_references_by_type(ref_type: str) -> list[Reference]:
    """Get all references of type ref_type from the repository."""
    with db.session.begin():
        ref_query = text("SELECT citation_key FROM reference_entries WHERE reference_type = :ref_type")
        res = db.session.execute(ref_query, {"ref_type": ref_type})

        return [Reference(
            type=ref_type,
            citation_key=row[0],
            fields=_get_fields(row[0])
        ) for row in res.fetchall()]


def _get_fields(reference_key: str) -> dict[str, str]:
    """Helper function. Will not handle transactions on it's own."""
    query = text("SELECT name, value FROM reference_fields WHERE reference_key = :ref_key ")
    res = db.session.execute(query, {"ref_key": reference_key})
    return {field_row[0]: field_row[1] for field_row in res.fetchall()}


def add_reference(reference: Reference) -> None:
    """Add a reference (including it's fields) to the repository."""
    with db.session.begin():
        query = text("""
            INSERT INTO reference_entries (reference_type, citation_key) VALUES (:type, :key)
        """)
        db.session.execute(query, {
            "type": reference.type,
            "key": reference.citation_key
        })
        _add_fields(reference.citation_key, reference.fields)


def _add_fields(reference_key: str, fields: dict[str, str]) -> None:
    """Helper function. Will not handle transactions on it's own."""
    query = text("""
        INSERT INTO reference_fields (reference_key, name, value) VALUES (:ref_key, :name, :value)
    """)
    for name, value in fields.items():
        db.session.execute(query, {
            "ref_key": reference_key,
            "name": name,
            "value": value
        })


def create_reference(typ: str, citation_key: str, fields: dict[str, str]) -> None:
    """Utility function. Equivalent to add_reference(Reference(typ, citation_key, fields))"""
    add_reference(Reference(typ, citation_key, fields))


def update_reference(citation_key: str, fields: dict[str, str]) -> None:
    """Add/update given fields of a reference. Other fields left as they are."""
    with db.session.begin():
        query = text("""
            INSERT INTO reference_fields (reference_key, name, value)
            VALUES (:ref_key, :name, :value)
            ON CONFLICT (reference_key, name) DO UPDATE SET value = excluded.value
        """)
        for name, value in fields.items():
            db.session.execute(query, {
                "ref_key": citation_key,
                "name": name,
                "value": value or None
            })


def delete_reference(citation_key: str) -> None:
    """Delete a reference (including it's fields) from the repository."""
    with db.session.begin():
        query = text("DELETE FROM reference_entries WHERE citation_key = :ref_key")
        db.session.execute(query, {"ref_key": citation_key})
