"""Book domain model."""


class Book:
    """Represents one book inside the personal digital library."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        genre: str,
        year: int,
        reading_status: str,
        progress: int,
    ) -> None:
        self.id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.reading_status = reading_status
        self.progress = progress

    def to_dict(self) -> dict:
        """Return a serializable representation of the book."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "reading_status": self.reading_status,
            "progress": self.progress,
        }

    def matches_query(self, query: str) -> bool:
        """Check whether the book matches a simple text search."""
        if query is None:
            return False

        normalized_query = query.strip().lower()
        if not normalized_query:
            return False

        return (
            normalized_query in str(self.id)
            or normalized_query in self.title.lower()
            or normalized_query in self.author.lower()
            or normalized_query in self.genre.lower()
            or normalized_query in self.reading_status.lower()
            or normalized_query in str(self.year)
        )
