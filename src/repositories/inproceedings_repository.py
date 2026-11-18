from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_inproceedings_references():
    query = text("SELECT author, title, booktitle, year, pages FROM inproceedings")
    res = db.session.execute(query)
    return [Reference("inproceedings", "", {
        "author": row[0],
        "title": row[1],
        "booktitle": row[2],
        "year": row[3],
        "pages": row[4] or ""
    }) for row in res.fetchall()]

def add_inproceedings_reference(author, title, booktitle, year, pages=""):
    query = text("""
        INSERT INTO inproceedings (author, title, booktitle, year, pages)
        values (:author, :title, :booktitle, :year, :pages)
    """)

    params = {
        "author":author,
        "title":title,
        "booktitle":booktitle,
        "year": year,
        "pages": pages
    }
    try:
        db.session.execute(query, params)
        db.session.commit()
    except  Exception:
        db.session.rollback()
        raise

