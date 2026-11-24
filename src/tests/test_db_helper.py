import unittest

from config import app
from db_helper import SEED_REFERENCES, seed_db, setup_db
from repositories.reference_repository import get_references

class TestDbHelper(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_seed_twice_adds_references_once(self):
        with app.app_context():
            seed_db()
            seed_db()
            refs = sorted(get_references(), key=lambda ref: ref.citation_key)
            expected = sorted(SEED_REFERENCES, key=lambda ref: ref.citation_key)
            self.assertEqual(refs, expected)
