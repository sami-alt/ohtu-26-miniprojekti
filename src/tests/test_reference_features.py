import unittest

from config import db, app
from db_helper import setup_db
from entities.reference import Reference
from repositories.book_repositories import add_book_reference
from repositories.reference_repository import get_references, delete_reference

class TestReferenceFeatures(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_add_get_delete(self):
        with app.app_context():
            test_fields = {
                "author": "Tove Jansson",
                "title": "Moominvalley in November",
                "publisher": "Farrar, Straus and Giroux",
                "year": "2003"
            }
            add_book_reference(**test_fields)
            res = get_references()
            self.assertSequenceEqual(res, [Reference("book", "", test_fields)])
            delete_reference(res[0].citation_key)
            res_after_delete = get_references()
            self.assertSequenceEqual(res_after_delete, [])