"""This module is deprecated"""

import uuid

from config import db
from sqlalchemy import text

from entities.reference import Reference
import repositories.reference_repository as refrep

def get_inproceedings_references():
    refs = refrep.get_references_by_type("inproceedings")

    # Strip citation keys for ✨backwards-compability✨
    for ref in refs:
        ref.citation_key = ""

    return refs


def add_inproceedings_reference(author, title, booktitle, year, pages=""):
    ref = Reference("inproceedings", str(uuid.uuid4()), {
        "author": author,
        "title": title,
        "booktitle": booktitle,
        "year": year,
        "pages": pages
    })
    refrep.add_reference(ref)
