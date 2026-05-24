from fastapi import APIRouter, Path, HTTPException
from schemas.book import Book, books
from typing import Annotated
from schemas.review import Review

from schemas.review import Review

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/")
def get_all_books(
        sort: Annotated[bool, Query(description="Sort by book's review.")] = False
) -> list[Book]:
    """Return a list of all available books."""
    if sort:
        sorted(books.values(), key=lambda book: book.review)
    else:
        return list(books.values())


@books_router.get("/{id}")
def get_book_by_id(
        id: Annotated[int, Path(description="Book's id to get.")]
) -> Book:
    """Return a book by id."""
    try:
        return books[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found.")


@books_router.post("/{id}/review")
def add_review(
        id: Annotated[int, Path(description="Book's id to get.")],
        review: Review
):
    """Add a review to book."""
    try:
        books[id].review = review.review
        return "Review added successfully."
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found.")



@books_router.post("/")
def add_book(book: Book):
    """Add a new book to the database."""
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book already exists.")
    else:
        books[book.id] = book
        return "Book added successfully."


@books_router.put("/{id}")
def replace_book(
        id: Annotated[int, Path(description="Book's id to get.")],
        book: Book
):
    """Replace a book by id."""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found.")
    else:
        books[id] = book
        return "Book replaced successfully."


@books_router.patch("/{id}")
def update_book(
        id: Annotated[int, Path(description="Book's id to get.")],
        book: Book
):
    """Update a book by id."""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found.")
    else:
        books[id] = book
        return "Book updated successfully."




@books_router.delete("/{id}")
def delete_book(
        id: Annotated[int, Path(description="Book's id to get.")],
        book: Book
):
    """Deletes a book by id."""
    if id in books:
        del books[id]
        return "Book deleted successfully."
    else:
        raise HTTPException(status_code=404, detail="Book not found.")





@books_router.delete("/")
def delete_all_books():
    """Delete all books."""
    books.clear()
    return "All books deleted successfully."
