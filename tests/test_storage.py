from datetime import datetime
from pathlib import Path

from pagetrail.model import Book, ReadingSession
from pagetrail.storage import Storage


def test_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "books.json"
    storage = Storage(path)
    created = datetime(2021, 2, 14, 9, 12, 3)
    book = Book(id="test", title="Demo", author="Someone", total_pages=120, added_at=created)
    book.sessions.append(
        ReadingSession(
            book_id="test",
            pages_read=15,
            created_at=datetime(2021, 2, 15, 10, 1, 27),
            note="morning",
        )
    )

    storage.save({"test": book})
    loaded = storage.load()

    assert "test" in loaded
    loaded_book = loaded["test"]
    assert loaded_book.title == "Demo"
    assert loaded_book.sessions[0].pages_read == 15

