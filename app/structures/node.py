"""Node definition for the doubly linked list."""

from __future__ import annotations

from app.models.book import Book


class Node:
    """Stores one book and its links to neighboring nodes."""

    def __init__(self, book: Book) -> None:
        self.book = book
        self.prev: Node | None = None
        self.next: Node | None = None
