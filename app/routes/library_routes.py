"""Flask routes for the digital library dashboard and actions."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.library_service import LibraryService


library_blueprint = Blueprint("library", __name__)
library_service = LibraryService()


@library_blueprint.route("/", methods=["GET"])
def home():
    """Render the main dashboard with the current state of the library."""
    context = library_service.get_dashboard_context()
    context["search_results"] = None
    return render_template("dashboard.html", **context)


@library_blueprint.route("/add", methods=["POST"])
def add_book():
    """Add a book to the start or end of the library."""
    placement = request.form.get("placement", "end").strip().lower()

    try:
        if placement == "start":
            library_service.prepend_book(request.form)
            flash("Book added at the start of the library.", "success")
        else:
            library_service.append_book(request.form)
            flash("Book added at the end of the library.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/insert", methods=["POST"])
def insert_book():
    """Insert a book at a specific zero-based position."""
    try:
        position = int(request.form.get("position", "0"))
        library_service.insert_book_at(position, request.form)
        flash(f"Book inserted at position {position}.", "success")
    except (ValueError, TypeError) as error:
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
        else:
            book_id = int(request.form.get("id", "0"))
            removed = library_service.remove_by_id(book_id)

        if removed is None:
            flash("No matching book was found.", "warning")
        else:
            flash(f"Removed book: {removed.title}.", "success")
    except (ValueError, TypeError) as error:
        flash(str(error), "error")

    return redirect(url_for("library.home"))


@library_blueprint.route("/navigate", methods=["POST"])
def navigate():
    """Move the current pointer forward or backward."""
    direction = request.form.get("direction", "").strip().lower()

    if direction == "next":
        book = library_service.move_next()
        flash(
            f"Current book: {book.title}." if book else "The library is empty.",
            "info",
        )
    elif direction == "previous":
        book = library_service.move_previous()
        flash(
            f"Current book: {book.title}." if book else "The library is empty.",
            "info",
        )
    else:
        flash("Invalid navigation direction.", "error")

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

    return render_template("dashboard.html", **context)
