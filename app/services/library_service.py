"""Business logic layer for the digital book library."""

from __future__ import annotations

from app.models.book import Book
from app.structures.doubly_linked_list import DoublyLinkedList


class LibraryService:
    """Coordinates validation, book creation, and linked list operations."""

    ALLOWED_STATUSES = {"Pending", "Reading", "Finished"}

    def __init__(self) -> None:
        self.library = DoublyLinkedList()
        self._next_id = 1

    def append_book(self, data: dict) -> Book:
        """Create a book and append it to the end of the library."""
        book = self._build_book(data)
        return self.library.append_book(book)

    def prepend_book(self, data: dict) -> Book:
        """Create a book and prepend it to the start of the library."""
        book = self._build_book(data)
        return self.library.prepend_book(book)

    def insert_book_at(self, position: int, data: dict) -> Book:
        """Create a book and insert it at a specific zero-based position."""
        book = self._build_book(data)
        return self.library.insert_book_at(position, book)

    def remove_by_id(self, book_id: int) -> Book | None:
        """Remove a book by its unique ID."""
        return self.library.remove_by_id(book_id)

    def remove_by_title(self, title: str) -> Book | None:
        """Remove a book by exact title match."""
        if not title or not title.strip():
            raise ValueError("Title is required.")
        return self.library.remove_by_title(title)

    def move_next(self) -> Book | None:
        """Move the current pointer forward."""
        return self.library.move_next()

    def move_previous(self) -> Book | None:
        """Move the current pointer backward."""
        return self.library.move_previous()

    def get_current(self) -> Book | None:
        """Return the current selected book."""
        return self.library.get_current()

    def get_all_forward(self) -> list[Book]:
        """Return all books from head to tail."""
        return self.library.get_all_forward()

    def get_all_backward(self) -> list[Book]:
        """Return all books from tail to head."""
        return self.library.get_all_backward()

    def search(self, query: str) -> list[Book]:
        """Search books using a simple text query."""
        if not query or not query.strip():
            return []
        return self.library.search(query)

    def count(self) -> int:
        """Return the total number of books in the library."""
        return self.library.count()

    def get_dashboard_context(self) -> dict:
        """Collect all data needed by the main dashboard template."""
        return {
            "current_book": self.get_current(),
            "books_forward": self.get_all_forward(),
            "books_backward": self.get_all_backward(),
            "book_count": self.count(),
        }

    def _build_book(self, data: dict) -> Book:
        """Validate request data and create a Book instance."""
        title = data.get("title", "").strip()
        author = data.get("author", "").strip()
        genre = data.get("genre", "").strip()
        status = data.get("reading_status", "").strip().title()

        if not title:
            raise ValueError("Title is required.")
        if not author:
            raise ValueError("Author is required.")
        if not genre:
            raise ValueError("Genre is required.")
        if status not in self.ALLOWED_STATUSES:
            raise ValueError("Reading status must be Pending, Reading, or Finished.")

        try:
            year = int(data.get("year", 0))
        except (TypeError, ValueError) as error:
            raise ValueError("Year must be a valid number.") from error

        try:
            progress = int(data.get("progress", 0))
        except (TypeError, ValueError) as error:
            raise ValueError("Progress must be a valid number.") from error

        if year <= 0:
            raise ValueError("Year must be greater than 0.")
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be between 0 and 100.")

        book = Book(
            book_id=self._next_id,
            title=title,
            author=author,
            genre=genre,
            year=year,
            reading_status=status,
            progress=progress,
        )
        self._next_id += 1
        return book
