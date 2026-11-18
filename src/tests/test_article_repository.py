import unittest

from config import app
from db_helper import setup_db
from entities.reference import Reference
from repositories.article_repository import add_article, get_articles


class TestArticleRepository(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            setup_db()

    def test_add_get(self):
        with app.app_context():
            test_fields = {
                "title": "Software Testing",
                "author": "Ada Lovelace",
                "year": 2026,
                "journal": "Journal of Testing",
                "volume": "12",
                "number": "3",
                "pages": "10-20",
            }
            add_article(**test_fields)
            articles = get_articles()
            self.assertSequenceEqual(articles, [Reference("article", "", {
                "author": "Ada Lovelace",
                "title": "Software Testing",
                "journal": "Journal of Testing",
                "year": 2026,
                "volume": "12",
                "number": "3",
                "pages": "10-20",
            })])
