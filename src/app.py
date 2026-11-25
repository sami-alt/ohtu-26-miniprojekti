import uuid

from flask import abort, flash, jsonify, redirect, render_template, request
from sqlalchemy.exc import DBAPIError

from config import app, test_env
from db_helper import reset_db, seed_db
from repositories.reference_repository import (
    create_reference,
    delete_reference,
    get_references,
    update_reference,
)
from repositories.reference_type_repository import (
    get_reference_type
)

SOURCE_TYPES = {
    "book": {
        "label": "Book",
        "title": "Add a book",
        "page_title": "Add book",
        "action": "/create_source/book",
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
        "action": "/create_source/article",
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
        "action": "/create_source/inproceedings",
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


@app.route("/create_source/<source_type>", methods=["POST"])
def create_source(source_type: str):
    ref_type = get_reference_type(source_type)
    if not ref_type:
        abort(404)

    field_names = ref_type.required_fields + ref_type.optional_fields
    fields =  {}
    for field_name in field_names:
        value = request.form.get(field_name)
        if value:
            fields[field_name] = value

    try:
        create_reference(source_type, str(uuid.uuid4()), fields)
    except DBAPIError as err:
        flash(str(err))
        return redirect("/create_source")

    return redirect("/")


@app.route("/new_<source_type>")
def new_anything(source_type: str):
    return redirect(f"/new_source?type={source_type}")


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

        update_reference(citation_key, fields)
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


@app.route("/seed")
def seed_database():
    seed_db()
    return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
