from flask import abort, flash, jsonify, redirect, render_template, request

from config import app, test_env
from db_helper import reset_db
from entities.reference import Reference
from repositories.article_repository import add_article
from repositories.book_repositories import add_book_reference
from repositories.inproceedings_repository import add_inproceedings_reference
from repositories.reference_repository import (
    delete_reference,
    get_references,
    replace_reference,
)

SOURCE_TYPES = {
    "book": {
        "label": "Book",
        "title": "Add a book",
        "page_title": "Add book",
        "action": "/create_book",
        "submit_label": "Add book",
        "fields": [
            {
                "name": "author",
                "label": "Author",
                "type": "text",
                "required": True,
            },
            {
                "name": "title",
                "label": "Title",
                "type": "text",
                "required": True,
            },
            {
                "name": "publisher",
                "label": "Publisher",
                "type": "text",
                "required": True,
            },
            {
                "name": "year",
                "label": "Year",
                "type": "number",
                "required": True,
            },
        ],
    },
    "article": {
        "label": "Journal article",
        "title": "Add a journal article",
        "page_title": "Add a journal article",
        "action": "/create_article",
        "submit_label": "Add article",
        "fields": [
            {
                "name": "author",
                "label": "Author",
                "type": "text",
                "required": True,
            },
            {
                "name": "title",
                "label": "Title",
                "type": "text",
                "required": True,
            },
            {
                "name": "journal",
                "label": "Journal",
                "type": "text",
                "required": True,
            },
            {
                "name": "year",
                "label": "Year",
                "type": "number",
                "required": True,
            },
            {
                "name": "volume",
                "label": "Volume",
                "type": "text",
                "required": False,
            },
            {
                "name": "number",
                "label": "Number",
                "type": "text",
                "required": False,
            },
            {
                "name": "pages",
                "label": "Pages",
                "type": "text",
                "required": False,
            },
        ],
    },
    "inproceedings": {
        "label": "Conference paper",
        "title": "Add a conference paper",
        "page_title": "Add a conference paper",
        "action": "/create_inproceedings",
        "submit_label": "Add a conference paper",
        "fields": [
            {
                "name": "author",
                "label": "Author",
                "type": "text",
                "required": True,
            },
            {
                "name": "title",
                "label": "Title",
                "type": "text",
                "required": True,
            },
            {
                "name": "booktitle",
                "label": "Conference proceedings title",
                "type": "text",
                "required": True,
            },
            {
                "name": "year",
                "label": "Year",
                "type": "number",
                "required": True,
            },
            {
                "name": "pages",
                "label": "Pages",
                "type": "text",
                "required": False,
            },
        ],
    },
}


def _render_source_form(source_type=None):
    source = SOURCE_TYPES.get(source_type)
    return render_template(
        "new_source.html",
        source=source,
        source_type=source_type,
        source_types=SOURCE_TYPES,
        page_title=source["page_title"] if source else "Add source",
    )


def _render_modify_source_form(source_type=None, citation_key=None, reference=None):
    source = SOURCE_TYPES.get(source_type)
    return render_template(
        "modify_source.html",
        source=source,
        source_type=source_type,
        source_types=SOURCE_TYPES,
        page_title=source["page_title"] if source else "Add source",
        citation_key=citation_key,
        reference=reference,
    )


@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)


@app.route("/new_source", methods=["GET"])
def choose_source_type():
    source_type = request.args.get("type")
    if source_type and source_type not in SOURCE_TYPES:
        abort(404)
    return _render_source_form(source_type)


@app.route("/new_inproceedings")
def new_inproceedings():
    return _render_source_form("inproceedings")


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
                "Author, title, conference proceedings title, and year " \
                "are required."
            )
        int(year)
        add_inproceedings_reference(author, title, booktitle, year, pages)
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error))
        return redirect("/new_inproceedings")


@app.route("/new_book")
def new_book():
    return _render_source_form("book")


@app.route("/create_book", methods=["POST"])
def add_book_to_references():
    author = request.form.get("author")
    title = request.form.get("title")
    publisher = request.form.get("publisher")
    year = request.form.get("year")

    try:
        add_book_reference(author, title, publisher, year)
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error))
        return redirect("/new_book")


@app.route("/new_article")
def new_article():
    return _render_source_form("article")


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
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error))
        return redirect("/new_article")


@app.route("/modify_reference_by_citation_key/<citation_key>", methods=["POST"])
def modify_reference(citation_key):
    references = get_references()
    reference_by_citation_key = next(
        (ref for ref in references if ref.citation_key == citation_key),
        None,
    )
    if reference_by_citation_key is None:
        flash(f"No reference found with citation key: {citation_key}")
        return redirect("/")

    return _render_modify_source_form(
        source_type=reference_by_citation_key.type,
        citation_key=citation_key,
        reference=reference_by_citation_key,
    )


@app.route(
    "/modify_reference/<citation_key>",
    methods=["POST"],
)
def modify_reference_by_citation_key(citation_key):
    try:
        references = get_references()
        existing = next(
            (ref for ref in references if ref.citation_key == citation_key),
            None,
        )
        if existing is None:
            raise ValueError(f"No reference found with citation key: {citation_key}")

        source = SOURCE_TYPES.get(existing.type)
        if source is None:
            raise ValueError(f"Unknown reference type: {existing.type}")

        fields = {}
        for field in source["fields"]:
            value = request.form.get(field["name"], "").strip()
            if field["required"] and not value:
                raise ValueError(f"{field['label']} is required.")
            fields[field["name"]] = value

        if "year" in fields:
            int(fields["year"])

        replace_reference(
            citation_key,
            Reference(existing.type, citation_key, fields),
        )
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error))
        return redirect("/")


@app.route(
    "/delete_reference_by_citation_key/<citation_key>",
    methods=["POST"],
)
def delete_reference_by_citation_key(citation_key):
    try:
        delete_reference(citation_key)
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error))
        return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
