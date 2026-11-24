"""This module is deprecated"""

import uuid

from entities.reference import Reference

import repositories.reference_repository as refrep

def get_book_references():
    refs = refrep.get_references_by_type("book")

    # Strip citation keys for ✨backwards-compability✨
    for ref in refs:
        ref.citation_key = ""

    return refs


def add_book_reference(author, title, publisher, year):
    ref = Reference("book", str(uuid.uuid4()), {
        "author": author,
        "title": title,
        "publisher": publisher,
        "year": year,
    })
    refrep.add_reference(ref)
