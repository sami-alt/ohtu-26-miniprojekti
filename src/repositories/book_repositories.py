from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_book_references():
    query = text("SELECT author, title, publisher, year FROM books")
    res = db.session.execute(query)
    return [Reference("book", "", {
        "author": row[0],
        "title": row[1],
        "publisher": row[2],
        "year": row[3]
    }) for row in res.fetchall()]

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


