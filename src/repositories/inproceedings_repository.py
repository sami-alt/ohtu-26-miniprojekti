from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_inproceedings_references():
    query = text("SELECT author, title, booktitle, year FROM inproceedings")
    res = db.session.execute(query)
    return [Reference("inproceedings", "", {
        "author": row[0],
        "title": row[1],
        "booktitle": row[2],
        "year": row[3]
    }) for row in res.fetchall()]

def add_inproceedings_reference(author, title, booktitle, year):
    query = text("""
        INSERT INTO inproceedings (author, title, booktitle, year)
        values (:author, :title, :booktitle, :year)
    """)

    params = {
        "author":author,
        "title":title,
        "booktitle":booktitle,
        "year": year
    }
    try:
        db.session.execute(query, params)
        db.session.commit()
    except  Exception:
        db.session.rollback()
        raise


