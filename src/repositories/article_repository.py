"""This module is deprecated"""

import uuid

from entities.reference import Reference
import repositories.reference_repository as refrep


def add_article(title, author, year, journal, volume, number, pages):
    ref = Reference("article", str(uuid.uuid4()), {
        "author": author,
        "title": title,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": number,
        "pages": pages
    })

    refrep.add_reference(ref)


def get_articles():
    refs = refrep.get_references_by_type("article")

    # Strip citation keys for ✨backwards-compability✨
    for ref in refs:
        ref.citation_key = ""

    return refs
