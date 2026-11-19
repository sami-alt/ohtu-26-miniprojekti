import unittest

from config import db, app
from db_helper import setup_db
from entities.reference import Reference
import repositories.reference_repository as refrep

class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    test_refs = [
        Reference(
            type="article",
            citation_key="smith2024",
            fields={
                "author": "Jane Smith",
                "title": "A Study of Example Systems",
                "journal": "Journal of Dummy Research",
                "year": "2024",
            },
        ),
        Reference(
            type="book",
            citation_key="doe2023",
            fields={
                "author": "John Doe",
                "title": "The Book of Examples",
                "publisher": "Example Press",
                "year": "2023",
            },
        ),
        Reference(
            type="inproceedings",
            citation_key="lee2025",
            fields={
                "author": "Alex Lee",
                "title": "An Example Conference Paper",
                "booktitle": "Proceedings of the Dummy Conference",
                "year": "2025",
            },
        ),
    ]

    def test_add_get(self):
        with app.app_context():
            for ref in self.test_refs:
                refrep.add_reference(ref)
            res = refrep.get_references()
            self.assertSequenceEqual(res, self.test_refs)

    def test_empty_get(self):
        with app.app_context():
            res = refrep.get_references()
            self.assertSequenceEqual(res, [])

    def test_get_by_type(self):
        with app.app_context():
            for ref in self.test_refs:
                refrep.add_reference(ref)
            res = refrep.get_references_by_type("article")
            cmp = filter(lambda x: x.type == "article", self.test_refs)
            self.assertSequenceEqual(res, list(cmp))
        
