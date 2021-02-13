import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .model import Book, ReadingSession


class Storage:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> Dict[str, Book]:
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        books: Dict[str, Book] = {}
        for book_id, payload in raw.items():
            book = Book(
                id=book_id,
                title=payload["title"],
                author=payload.get("author"),
                total_pages=payload.get("total_pages"),
                added_at=datetime.fromisoformat(payload["added_at"]),
            )
            for s in payload.get("sessions", []):
                session = ReadingSession(
                    book_id=book_id,
                    pages_read=s["pages_read"],
                    created_at=datetime.fromisoformat(s["created_at"]),
                    note=s.get("note"),
                )
                book.sessions.append(session)
            books[book_id] = book
        return books

    def save(self, books: Dict[str, Book]) -> None:
        payload: Dict[str, Dict] = {}
        for book_id, book in books.items():
            payload[book_id] = {
                "title": book.title,
                "author": book.author,
                "total_pages": book.total_pages,
                "added_at": book.added_at.isoformat(),
                "sessions": [
                    {
                        **asdict(session),
                        "created_at": session.created_at.isoformat(),
                    }
                    for session in book.sessions
                ],
            }
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

