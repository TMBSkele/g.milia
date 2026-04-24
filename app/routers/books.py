from fastapi import APIRouter, Path, HTTPException
from schemas.book import Book, books
from typing import Annotated
from schemas.review import Review

from schemas.review import Review

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/")
def get_all_books() -> list[Book]:
    """Return a list of all available books."""
    return books.values()


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