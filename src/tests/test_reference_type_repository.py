import unittest

from config import app
from db_helper import setup_db
from entities.reference_type import ReferenceType
import repositories.reference_type_repository as reftyrep

class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_types_exist(self):
        with app.app_context():
            types = reftyrep.get_types()
            self.assertTrue(len(types))

    def test_get_type(self):
        with app.app_context():
            typ = reftyrep.get_type("article")
            self.assertIsNotNone(typ)

            assert typ is not None # For type hints

            self.assertEqual(typ.name, "article")
            self.assertTrue(len(typ.required_fields))
            self.assertTrue(len(typ.optional_fields))