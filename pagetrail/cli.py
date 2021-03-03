import argparse
from typing import Dict

from .model import Book, ReadingSession
from .config import get_data_dir
from .storage import Storage


def get_storage() -> Storage:
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return Storage(data_dir / "books.json")


def cmd_add(args: argparse.Namespace, storage: Storage, books: Dict[str, Book]) -> None:
    if args.id in books:
        raise SystemExit(f"Book with id '{args.id}' already exists.")
    books[args.id] = Book(
        id=args.id,
        title=args.title,
        author=args.author,
        total_pages=args.pages,
    )
    storage.save(books)
    print(f"Added book '{args.title}' with id '{args.id}'.")


def cmd_list(_: argparse.Namespace, __: Storage, books: Dict[str, Book]) -> None:
    if not books:
        print("No books yet.")
        return
    for book in books.values():
        total_pages = sum(s.pages_read for s in book.sessions)
        suffix = f", total={total_pages}" if total_pages else ""
        print(f"- {book.id}: {book.title} ({book.author or 'unknown'}){suffix}")


def cmd_summary(args: argparse.Namespace, __: Storage, books: Dict[str, Book]) -> None:
    book = books.get(args.id)
    if book is None:
        raise SystemExit(f"Unknown book id '{args.id}'.")
    if not book.sessions:
        print(f"No sessions for '{book.title}' yet.")
        return
    total_pages = sum(s.pages_read for s in book.sessions)
    last = book.sessions[-1]
    print(f"{book.title} -> total={total_pages} pages, last={last.pages_read} pages")


def cmd_log(args: argparse.Namespace, storage: Storage, books: Dict[str, Book]) -> None:
    book = books.get(args.id)
    if book is None:
        raise SystemExit(f"Unknown book id '{args.id}'.")
    session = ReadingSession(book_id=book.id, pages_read=args.pages, note=args.note)
    book.sessions.append(session)
    storage.save(books)
    print(f"Logged {args.pages} pages for '{book.title}'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pagetrail", description="Simple reading tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new book")
    p_add.add_argument("id", help="Short identifier for the book")
    p_add.add_argument("title", help="Title of the book")
    p_add.add_argument("--author", help="Author name")
    p_add.add_argument("--pages", type=int, help="Total number of pages")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List existing books")
    p_list.set_defaults(func=cmd_list)

    p_log = sub.add_parser("log", help="Log a reading session")
    p_log.add_argument("id", help="Book id")
    p_log.add_argument("pages", type=int, help="Number of pages read")
    p_log.add_argument("--note", help="Optional short note")
    p_log.set_defaults(func=cmd_log)

    p_summary = sub.add_parser("summary", help="Show summary for a book")
    p_summary.add_argument("id", help="Book id")
    p_summary.set_defaults(func=cmd_summary)

    return parser


def main(argv: None | list[str] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = get_storage()
    books = storage.load()
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return
    func(args, storage, books)


if __name__ == "__main__":
    main()
