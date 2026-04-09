"""Manual doubly linked list implementation used as the main library storage."""

from __future__ import annotations

from app.models.book import Book
from app.structures.node import Node


class DoublyLinkedList:
    """Custom doubly linked list for storing and navigating books."""

    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.current: Node | None = None
        self.size = 0

    def is_empty(self) -> bool:
        """Return True when the library has no books."""
        return self.head is None

    def count(self) -> int:
        """Return the number of stored books."""
        return self.size

    def append_book(self, book: Book) -> Book:
        """Insert a book at the end of the list."""
        new_node = Node(book)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1
        return book

    def prepend_book(self, book: Book) -> Book:
        """Insert a book at the start of the list."""
        new_node = Node(book)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            assert self.head is not None
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1
        return book

    def insert_book_at(self, position: int, book: Book) -> Book:
        """Insert a book at a zero-based position."""
        if position < 0 or position > self.size:
            raise IndexError("Position is out of bounds.")

        if position == 0:
            return self.prepend_book(book)
        if position == self.size:
            return self.append_book(book)

        current_node = self._get_node_at(position)
        previous_node = current_node.prev
        new_node = Node(book)

        new_node.prev = previous_node
        new_node.next = current_node

        if previous_node is not None:
            previous_node.next = new_node
        current_node.prev = new_node

        self.size += 1
        return book

    def remove_by_id(self, book_id: int) -> Book | None:
        """Remove the first book with the provided ID."""
        node = self.head

        while node is not None:
            if node.book.id == book_id:
                return self._unlink_node(node)
            node = node.next

        return None

    def remove_by_title(self, title: str) -> Book | None:
        """Remove the first book whose title matches the given text."""
        normalized_title = title.strip().lower()
        node = self.head

        while node is not None:
            if node.book.title.strip().lower() == normalized_title:
                return self._unlink_node(node)
            node = node.next

        return None

    def move_next(self) -> Book | None:
        """Move the current pointer forward and return the current book."""
        if self.current is None:
            return None
        if self.current.next is not None:
            self.current = self.current.next
        return self.current.book

    def move_previous(self) -> Book | None:
        """Move the current pointer backward and return the current book."""
        if self.current is None:
            return None
        if self.current.prev is not None:
            self.current = self.current.prev
        return self.current.book

    def get_current(self) -> Book | None:
        """Return the current selected book."""
        if self.current is None:
            return None
        return self.current.book

    def get_all_forward(self) -> list[Book]:
        """Return all books from head to tail."""
        books: list[Book] = []
        node = self.head

        while node is not None:
            books.append(node.book)
            node = node.next

        return books

    def get_all_backward(self) -> list[Book]:
        """Return all books from tail to head."""
        books: list[Book] = []
        node = self.tail

        while node is not None:
            books.append(node.book)
            node = node.prev

        return books

    def search(self, query: str) -> list[Book]:
        """Return every book that matches the provided query."""
        matches: list[Book] = []
        node = self.head

        while node is not None:
            if node.book.matches_query(query):
                matches.append(node.book)
            node = node.next

        return matches

    def _get_node_at(self, position: int) -> Node:
        """Return the node located at a zero-based position."""
        if position < 0 or position >= self.size:
            raise IndexError("Position is out of bounds.")

        if position <= self.size // 2:
            index = 0
            node = self.head
            while index < position:
                assert node is not None
                node = node.next
                index += 1
        else:
            index = self.size - 1
            node = self.tail
            while index > position:
                assert node is not None
                node = node.prev
                index -= 1

        assert node is not None
        return node

    def _unlink_node(self, node: Node) -> Book:
        """Detach a node from the list and return its book."""
        previous_node = node.prev
        next_node = node.next

        if previous_node is not None:
            previous_node.next = next_node
        else:
            self.head = next_node

        if next_node is not None:
            next_node.prev = previous_node
        else:
            self.tail = previous_node

        if self.current is node:
            self.current = next_node if next_node is not None else previous_node

        node.prev = None
        node.next = None
        self.size -= 1

        if self.size == 0:
            self.head = None
            self.tail = None
            self.current = None

        return node.book
