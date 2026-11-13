from config import db
from sqlalchemy import text

def add_book_reference(author, title, publisher, year):
    query = text("""
        INSERT INTO books (author, title, publisher,year)
        values (:author, :title, :publisher, :year)
    """)

    params = {
        "author":author,
        "title":title,
        "publisher":publisher,
        "year": year
    }
    try:
        db.session.execute(query, params)
        db.session.commit()
    except  Exception:
        db.session.rollback()
        raise


