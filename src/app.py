from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.book_repositories import add_book_reference, get_book_references
from repositories.article_repository import add_article, get_articles
from repositories.inproceedings_repository import (
    add_inproceedings_reference,
    get_inproceedings_references,
)
from config import app, test_env

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_inproceedings")
def new_inproceedings():
    return render_template("new_inproceedings.html")

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
        return redirect("/source_listing")
    except Exception as error:
        flash(str(error))
        return redirect("/new_inproceedings")

@app.route("/new_book")
def new_book():
    return render_template("new_book.html")

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
    return render_template("new_article.html")

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

@app.route("/source_listing")
def source_listing():
    references = get_book_references() + get_articles() + get_inproceedings_references()
    return render_template("source_listing.html", references=references)

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
