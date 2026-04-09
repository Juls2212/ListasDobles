"""Flask routes for the digital library dashboard and actions."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.library_service import LibraryService
from app.utils.exceptions import (
    BookNotFoundError,
    EmptyLibraryError,
    NavigationError,
    ValidationError,
)


library_blueprint = Blueprint("library", __name__)
library_service = LibraryService()


@library_blueprint.route("/", methods=["GET"])
def home():
    """Render the main dashboard with the current state of the library."""
    context = library_service.get_dashboard_context()
    context["search_results"] = None
    context["search_query"] = ""
    return render_template("index.html", **context)


@library_blueprint.route("/add", methods=["GET", "POST"])
def add_book():
    """Add a book to the start or end of the library."""
    if request.method == "GET":
        return render_template("add.html")

    placement = request.form.get("placement", "end").strip().lower()

    try:
        if placement == "start":
            library_service.prepend_book(request.form)
            flash("Book added at the start of the library.", "success")
        elif placement == "end":
            library_service.append_book(request.form)
            flash("Book added at the end of the library.", "success")
        else:
            raise ValidationError("Placement must be either start or end.")
    except ValidationError as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/insert", methods=["POST"])
def insert_book():
    """Insert a book at a specific zero-based position."""
    try:
        raw_position = request.form.get("position", "").strip()
        if not raw_position:
            raise ValidationError("Position is required.")
        position = int(raw_position)
        library_service.insert_book_at(position, request.form)
        flash(f"Book inserted at position {position}.", "success")
    except (ValidationError, TypeError) as error:
        flash(str(error), "error")
    except IndexError as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/delete", methods=["POST"])
def delete_book():
    """Delete a book either by ID or by title."""
    delete_type = request.form.get("delete_type", "id").strip().lower()

    try:
        if delete_type == "title":
            title = request.form.get("title", "")
            removed = library_service.remove_by_title(title)
        elif delete_type == "id":
            raw_book_id = request.form.get("id", "").strip()
            if not raw_book_id:
                raise ValidationError("Book ID is required.")
            book_id = int(raw_book_id)
            removed = library_service.remove_by_id(book_id)
        else:
            raise ValidationError("Delete type must be id or title.")

        flash(f"Removed book: {removed.title}.", "success")
    except (ValidationError, TypeError, EmptyLibraryError, BookNotFoundError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/navigate", methods=["POST"])
def navigate():
    """Move the current pointer forward or backward."""
    direction = request.form.get("direction", "").strip().lower()

    try:
        if direction == "next":
            book = library_service.move_next()
        elif direction == "previous":
            book = library_service.move_previous()
        else:
            raise ValidationError("Invalid navigation direction.")

        flash(f"Current book: {book.title}.", "info")
    except (ValidationError, EmptyLibraryError, NavigationError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/search", methods=["GET", "POST"])
def search():
    """Search books and render the dashboard with search results."""
    query = request.values.get("query", "").strip()
    context = library_service.get_dashboard_context()
    context["search_results"] = library_service.search(query) if query else []
    context["search_query"] = query

    if query and not context["search_results"]:
        flash("No books matched the search.", "warning")
    elif query:
        flash(f'Found {len(context["search_results"])} matching book(s).', "info")

    return render_template("index.html", **context)
