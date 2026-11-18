import unittest

from config import db, app
from db_helper import setup_db
from entities.reference import Reference
from repositories.inproceedings_repository import add_inproceedings_reference, get_inproceedings_references

class TestInproceedingsRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_add_get(self):
        with app.app_context():
            test_fields = {
                "author": "Jove Tansson",
                "title": "Article about something scientific",
                "booktitle": "Proceedings of the Moomin Conference",
                "year": "2004",
                "pages": "1-10"
            }
            add_inproceedings_reference(**test_fields)
            res = get_inproceedings_references()
            self.assertSequenceEqual(res, [Reference("inproceedings", "", test_fields)])

    def test_pages_are_optional(self):
        with app.app_context():
            fields = {
                "author": "Jove Tansson",
                "title": "A conference paper",
                "booktitle": "Proceedings of the Moomin Conference",
                "year": "2004"
            }
            add_inproceedings_reference(**fields)
            self.assertSequenceEqual(
                get_inproceedings_references(),
                [Reference("inproceedings", "", {**fields, "pages": ""})]
            )