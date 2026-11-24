import os

from sqlalchemy import text

from config import db, app
from entities.reference import Reference
from repositories.reference_repository import add_reference

SEED_REFERENCES = [
    Reference("book", "martin2008", {
        "author": "Robert C. Martin",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "publisher": "Prentice Hall",
        "year": "2008",
    }),
    Reference("article", "dijkstra1968", {
        "author": "Edsger W. Dijkstra",
        "title": "Go To Statement Considered Harmful",
        "journal": "Communications of the ACM",
        "year": "1968",
        "volume": "11",
        "number": "3",
        "pages": "147--148",
    }),
    Reference("inproceedings", "royce1970", {
        "author": "Winston W. Royce",
        "title": "Managing the Development of Large Software Systems",
        "booktitle": "Proceedings of IEEE WESCON",
        "year": "1970",
        "pages": "1--9",
    }),
]


def seed_db():
    sql = text("SELECT citation_key FROM reference_entries")
    existing = {row[0] for row in db.session.execute(sql).fetchall()}
    for ref in SEED_REFERENCES:
        if ref.citation_key not in existing:
            add_reference(ref)


def reset_db():
    for table in tables():
        print(f"Clearing contents from table {table}")
        sql = text(f"DELETE FROM {table}")
        db.session.execute(sql)
    db.session.commit()

def tables():
    """Returns all table names from the database"""
    sql = text(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]

def setup_db():
    """
        Creating the database
        If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding="UTF-8") as f:
        schema_sql = f.read().strip()

    for stmt in schema_sql.split(';'):
        if stmt.strip():
            sql = text(stmt)
            db.session.execute(sql)
    db.session.commit()

    #sql = text(schema_sql)
    #db.session.execute(sql)
    #db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
