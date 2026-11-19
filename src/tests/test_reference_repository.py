import unittest

from config import db, app
from db_helper import setup_db
from entities.reference import Reference
import repositories.reference_repository as refrep

class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_add_get(self):
        with app.app_context():
            ref = Reference("book", "jansson03", {
                "author": "Tove Jansson",
                "title": "Moominvalley in November",
                "publisher": "Farrar, Straus and Giroux",
                "year": "2003"
            })
            refrep.add_reference(ref)
            res = refrep.get_references()
            self.assertSequenceEqual(res, [ref])