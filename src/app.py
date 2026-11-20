from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repositories import add_book_reference
from repositories.article_repository import add_article
from repositories.inproceedings_repository import add_inproceedings_reference

from repositories.reference_repository import delete_reference, get_references

from config import app, test_env

@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_source", methods=["GET"])
def choose_source_type():
    return render_template("source_type_selection.html")

@app.route("/new_inproceedings")
def new_inproceedings():
    return render_template(
        "new_source.html",
        title="Add a conference paper",
        page_title="Add a conference paper",
        action="/create_inproceedings",
        submit_label="Add a conference paper",
        fields=[
            {"name": "author", "label": "Author", "type": "text", "required": True},
            {"name": "title", "label": "Title", "type": "text", "required": True},
            {
                "name": "booktitle",
                "label": "Conference proceedings title",
                "type": "text",
                "required": True,
            },
            {"name": "year", "label": "Year", "type": "number", "required": True},
            {"name": "pages", "label": "Pages", "type": "text", "required": False},
        ],
    )

@app.route("/create_inproceedings", methods=["POST"])
def add_inproceedings_to_references():
    author = request.form.get("author", "").strip()
    title = request.form.get("title", "").strip()
    booktitle = request.form.get("booktitle", "").strip()
    year = request.form.get("year", "").strip()
    pages = request.form.get("pages", "").strip()

    try:
        if not author or not title or not booktitle or not year:
            raise ValueError(
                "Author, title, conference proceedings title, and year are required."
            )
        int(year)
        add_inproceedings_reference(author, title, booktitle, year, pages)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_inproceedings")

@app.route("/new_book")
def new_book():
    return render_template(
        "new_source.html",
        title="Add a book",
        page_title="Add book",
        action="/create_book",
        submit_label="Add book",
        fields=[
            {"name": "author", "label": "Author", "type": "text", "required": True},
            {"name": "title", "label": "Title", "type": "text", "required": True},
            {
                "name": "publisher",
                "label": "Publisher",
                "type": "text",
                "required": True,
            },
            {"name": "year", "label": "Year", "type": "number", "required": True},
        ],
    )

@app.route("/create_book", methods=["POST"])
def add_book_to_references():
    author = request.form.get("author")
    title = request.form.get("title")
    publisher = request.form.get("publisher")
    year = request.form.get("year")

    try:
        add_book_reference(author, title, publisher, year)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_book")

@app.route("/new_article")
def new_article():
    return render_template(
        "new_source.html",
        title="Add a journal article",
        page_title="Add a journal article",
        action="/create_article",
        submit_label="Add article",
        fields=[
            {"name": "author", "label": "Author", "type": "text", "required": True},
            {"name": "title", "label": "Title", "type": "text", "required": True},
            {"name": "journal", "label": "Journal", "type": "text", "required": True},
            {"name": "year", "label": "Year", "type": "number", "required": True},
            {"name": "volume", "label": "Volume", "type": "text", "required": False},
            {"name": "number", "label": "Number", "type": "text", "required": False},
            {"name": "pages", "label": "Pages", "type": "text", "required": False},
        ],
    )

@app.route("/create_article", methods=["POST"])
def add_article_to_references():
    author = request.form.get("author")
    title = request.form.get("title")
    journal = request.form.get("journal")
    year = request.form.get("year")
    volume = request.form.get("volume") or None
    number = request.form.get("number") or None
    pages = request.form.get("pages") or None

    try:
        add_article(title, author, year, journal, volume, number, pages)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_article")

@app.route("/delete_reference_by_citation_key/<citation_key>", methods=["POST"])
def delete_reference_by_citation_key(citation_key):
    try:
        delete_reference(citation_key)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/")


# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
