from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ReadingSession:
    book_id: str
    pages_read: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    note: Optional[str] = None


@dataclass
class Book:
    id: str
    title: str
    author: Optional[str] = None
    total_pages: Optional[int] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    sessions: List[ReadingSession] = field(default_factory=list)

