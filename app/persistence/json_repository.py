"""JSON persistence for the digital book library."""

from __future__ import annotations

import json
from pathlib import Path


class JsonLibraryRepository:
    """Persist the library state to a JSON file using atomic writes."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def save_data(self, payload: dict) -> None:
        """Save the library payload to disk without risking partial writes."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.file_path.with_suffix(f"{self.file_path.suffix}.tmp")

        with temp_path.open("w", encoding="utf-8") as json_file:
            json.dump(payload, json_file, ensure_ascii=False, indent=4)

        temp_path.replace(self.file_path)

    def load_data(self) -> dict:
        """Load the persisted library payload or return an empty state."""
        if not self.file_path.exists():
            return {"books": [], "current_book_id": None}

        with self.file_path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if not isinstance(data, dict):
            return {"books": [], "current_book_id": None}

        books = data.get("books", [])
        current_book_id = data.get("current_book_id")

        if not isinstance(books, list):
            books = []

        return {
            "books": books,
            "current_book_id": current_book_id,
        }
