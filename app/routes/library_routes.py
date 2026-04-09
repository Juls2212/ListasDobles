"""Flask routes for the digital library dashboard and actions."""

from __future__ import annotations

from typing import Any

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


def _build_dashboard_context(
    search_query: str = "",
    search_results: list | None = None,
) -> dict[str, Any]:
    """Build the shared template context for the dashboard."""
    context = library_service.get_dashboard_context()
    context["search_query"] = search_query
    context["search_results"] = search_results
    return context


def _render_dashboard(search_query: str = "", search_results: list | None = None):
    """Render the main dashboard with shared view data."""
    return render_template(
        "index.html",
        **_build_dashboard_context(
            search_query=search_query,
            search_results=search_results,
        ),
    )


@library_blueprint.route("/", methods=["GET"])
def home():
    """Render the main dashboard with the current state of the library."""
    return _render_dashboard()


@library_blueprint.route("/add", methods=["GET", "POST"])
def add_book():
    """Render the add page or add a book to the start or end of the library."""
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
    except (ValidationError, TypeError, IndexError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/delete", methods=["POST"])
def delete_book():
    """Delete a book either by ID or by title."""
    delete_type = request.form.get("delete_type", "id").strip().lower()

    try:
        if delete_type == "title":
            removed_book = library_service.remove_by_title(request.form.get("title", ""))
        elif delete_type == "id":
            raw_book_id = request.form.get("id", "").strip()
            if not raw_book_id:
                raise ValidationError("Book ID is required.")

            removed_book = library_service.remove_by_id(int(raw_book_id))
        else:
            raise ValidationError("Delete type must be id or title.")

        flash(f"Removed book: {removed_book.title}.", "success")
    except (ValidationError, TypeError, EmptyLibraryError, BookNotFoundError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/navigate", methods=["POST"])
def navigate():
    """Move the current pointer forward or backward."""
    direction = request.form.get("direction", "").strip().lower()

    try:
        if direction == "next":
            current_book = library_service.move_next()
        elif direction == "previous":
            current_book = library_service.move_previous()
        else:
            raise ValidationError("Invalid navigation direction.")

        flash(f"Current book: {current_book.title}.", "info")
    except (ValidationError, EmptyLibraryError, NavigationError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/search", methods=["POST"])
def search():
    """Search books and render the dashboard with matching results."""
    query = request.form.get("query", "").strip()
    results = library_service.search(query) if query else []

    if query and not results:
        flash("No books matched the search.", "warning")
    elif query:
        flash(f"Found {len(results)} matching book(s).", "info")
    else:
        flash("Enter a search term.", "warning")

    return _render_dashboard(search_query=query, search_results=results)
