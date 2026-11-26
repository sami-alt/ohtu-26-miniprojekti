import unittest

from app import app
from db_helper import setup_db
from entities.reference import Reference
from repositories.reference_repository import add_reference


class TestSourceSearchApi(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()
            add_reference(Reference("book", "north2031", {
                "author": "Mira AuthorNorth",
                "title": "FilterBookAlpha",
                "publisher": "FilterPressAlpha",
                "year": "2031",
            }))
            add_reference(Reference("article", "south2032", {
                "author": "Niko AuthorSouth",
                "title": "FilterArticleBeta",
                "journal": "FilterJournalBeta",
                "year": "2032",
            }))

    def test_filters_match_all_conditions_partially_and_case_insensitively(self):
        response = app.test_client().get(
            "/api/references?field=author&value=mira+author"
            "&field=year&value=2031"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [reference["citation_key"] for reference in response.json["references"]],
            ["north2031"],
        )

    def test_empty_filters_return_all_and_no_match_returns_empty_list(self):
        client = app.test_client()

        all_response = client.get("/api/references?field=author&value=+")
        no_match_response = client.get("/api/references?author=Nobody")

        self.assertEqual(len(all_response.json["references"]), 2)
        self.assertEqual(no_match_response.json["references"], [])
