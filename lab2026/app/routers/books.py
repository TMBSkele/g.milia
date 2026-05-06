from conda_package_streaming.url import session
from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import BookCreate, BookPublic, BookDB
from typing import Annotated
from schemas.review import Review
from data.db import SessionDep
from sqlmodel import select, delete

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/")
def get_all_books(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort by book's review.")] = False
) -> list[BookPublic]:
    """Return a list of all available books."""
    books = session.exec(select(BookDB)).all()
    if sort:
        return sorted(books, key=lambda book: book.review)
    else:
        return list(books)


@books_router.get("/{id}")
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="Book's id to get.")]
) -> BookPublic:
    """Return a book by id."""
    book = session.get(BookDB, id)

    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found.")


@books_router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="Book's id to get.")],
        review: Review
):
    """Add a review to book."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    book.review = review.review
    session.add(book)
    session.commit()
    return "Review added successfully."




@books_router.post("/")
def add_book(session:SessionDep, book: BookCreate):
    """Add a new book to the database."""
    book_entry = BookDB.model_validate(book)
    session.add(book_entry)
    session.commit()
    return "Book added successfully."


@books_router.put("/{id}")
def replace_book(
        session: SessionDep,
        id: Annotated[int, Path(description="Book's id to get.")],
        new_book: BookCreate
):
    """Replace a book by id."""
    book = session.get(BookDB, id)


    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.add(book)
    session.commit()
    return "Book replaced successfully."


@books_router.patch("/{id}")
def update_book(
        session : SessionDep,
        id: Annotated[int, Path(description="Book's id to get.")],
        updated_book: BookCreate
):
    """Update a book by id."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    book.title = updated_book.title
    book.author = updated_book.author
    book.review = updated_book.review
    session.add(book)
    session.commit()
    return "Book updated successfully."




@books_router.delete("/{id}")
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="Book's id to get.")],
):
    """Deletes a book by id."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    session.delete(book)
    session.commit()
    return "Book deleted successfully."



@books_router.delete("/")
def delete_all_books(session: SessionDep):
    """Delete all books."""
    session.exec(delete(BookDB))
    session.commit()
    return "All books deleted successfully."
