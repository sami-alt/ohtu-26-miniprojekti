import unittest

from app import app
from db_helper import setup_db
from repositories.book_repositories import add_book_reference
from repositories.inproceedings_repository import get_inproceedings_references

@unittest.skip("Old unported test. Possibly redundant with robot tests?")
class TestInproceedingsForm(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()
        self.client = app.test_client()

    def test_successful_submission_is_shown_in_source_listing(self):
        with app.app_context():
            add_book_reference(
                "Tove Jansson", "Moominvalley in November",
                "Farrar, Straus and Giroux", "2003"
            )

        response = self.client.post("/create_inproceedings", data={
            "author": "Jove Tansson",
            "title": "A conference paper",
            "booktitle": "Proceedings of the Moomin Conference",
            "year": "2004",
            "pages": "1-10"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        listing = self.client.get("/")
        for value in (
            "inproceedings",
            "Jove Tansson",
            "A conference paper",
            "2004",
            "Proceedings of the Moomin Conference",
            "1-10"
        ):
            self.assertIn(value.encode(), listing.data)
        for value in ("book", "Tove Jansson", "Moominvalley in November"):
            self.assertIn(value.encode(), listing.data)

    def test_pages_can_be_omitted(self):
        response = self.client.post("/create_inproceedings", data={
            "author": "Jove Tansson",
            "title": "A conference paper",
            "booktitle": "Proceedings of the Moomin Conference",
            "year": "2004"
        })

        self.assertEqual(response.status_code, 302)
        with app.app_context():
            self.assertEqual(get_inproceedings_references()[0].fields["pages"], "")

    def test_non_integer_year_is_rejected_without_saving(self):
        response = self.client.post("/create_inproceedings", data={
            "author": "Jove Tansson",
            "title": "A conference paper",
            "booktitle": "Proceedings of the Moomin Conference",
            "year": "twenty-four"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/new_inproceedings")
        with app.app_context():
            self.assertEqual(get_inproceedings_references(), [])
