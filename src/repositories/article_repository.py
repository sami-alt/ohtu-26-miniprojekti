from config import db
from sqlalchemy import text
from entities.reference import Reference


def add_article(title, author, year, journal, volume, number, pages):
    sql = text("INSERT INTO articles (author, title, journal, year, volume, number, pages) VALUES (:author, :title, :journal, :year, :volume, :number, :pages)")
    db.session.execute(sql, {"author": author, "title": title, "journal": journal, "year": year, "volume": volume, "number": number, "pages": pages})
    db.session.commit()

def get_articles():
    query = text("select author, title, journal, year, volume, number, pages from articles")
    result = db.session.execute(query)
    return [Reference("article", "",{
        "author": row[0], 
        "title": row[1], 
        "journal": row[2], 
        "year": row[3], 
        "volume": row[4],
        "number": row[5], 
        "pages": row[6]}) for row in result.fetchall()]