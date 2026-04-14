from fastapi import APIRouter, Query, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data_base.list_of_books import books_list
from pathlib import Path


router = APIRouter()
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# @router.get("/", response_class=HTMLResponse)
# async def html_books(
#     request: Request,
#     year: int = Query(None, description="Year of book"),
#     title: str = Query(None, description="Title of book"),
# ):
#     """Получить список книг."""
#     result = books_list

#     if year is not None:
#         result = [book for book in result if book.year == year]
#     if title is not None:
#         result = [book for book in result if book.title == title]

#     context = {
#         "request": request,
#         "books": result,
#         "title": 'Список книг'
#     }

#     return templates.TemplateResponse(request=request, name="books/books_list.html", context=context)


@router.get("/{book_id}", response_class=HTMLResponse, name='html_books_detail')
async def book_details(request: Request, book_id: int):
    """Получить детальную информацию о книге."""
    book_id -= 1

    if book_id < 0 or book_id >= len(books_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book = books_list[book_id]

    context = {
        "request": request,
        "book": book,
    }

    return templates.TemplateResponse(request=request, name="books/current_book.html", context=context)
