import unittest

from config import db, app
from db_helper import setup_db
from entities.reference import Reference
from repositories.book_repositories import add_book_reference, get_book_references
from repositories.reference_repository import get_references_by_type

class TestBookRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_add_get(self):
        with app.app_context():
            test_fields = {
                "author": "Tove Jansson",
                "title": "Moominvalley in November",
                "publisher": "Farrar, Straus and Giroux",
                "year": "2003"
            }
            add_book_reference(**test_fields)
            res = get_book_references()
            self.assertSequenceEqual(res, [Reference("book", "", test_fields)])

    def test_added_books_have_unique_citation_keys(self):
        with app.app_context():
            add_book_reference("Author One", "First Book", "Publisher", "2024")
            add_book_reference("Author Two", "Second Book", "Publisher", "2025")

            references = get_references_by_type("book")
            citation_keys = [reference.citation_key for reference in references]

            self.assertEqual(len(citation_keys), 2)
            self.assertTrue(all(citation_keys))
            self.assertNotEqual(citation_keys[0], citation_keys[1])
