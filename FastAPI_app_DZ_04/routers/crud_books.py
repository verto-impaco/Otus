from fastapi import APIRouter, Query, HTTPException, status
from data_base.list_of_books import Books, books_list


router = APIRouter()


@router.get("/", response_model=list[Books])
async def books(
    year: int = Query(None, description="Year of book"),
    title: str = Query(None, description="Title of book"),
):
    """Получить список книг."""
    result = books_list

    if year is not None:
        result = [book for book in result if book.year == year]
    if title is not None:
        result = [book for book in result if book.title == title]

    return result


@router.get("/{book_id}/", response_model=Books)
async def book_details(book_id: int):
    """Получить детальную информацию о книге."""
    book_id -= 1

    if book_id < 0 or book_id >= len(books_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return books_list[book_id]


@router.post("/", response_model=Books, status_code=status.HTTP_201_CREATED)
async def book_create(book: Books):
    """Добавить книгу."""
    for m in books_list:
        if m.title == book.title and m.year == book.year:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Book already exists")
    books_list.append(book)
    return book


@router.put("/{book_id}/", response_model=Books)
async def book_update(book_id: int, book: Books):
    """Обновить книгу."""
    book_id -= 1

    if book_id < 0 or book_id >= len(books_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    books_list[book_id].title = book.title
    books_list[book_id].year = book.year

    return books_list[book_id]


@router.delete("/{book_id}/")
async def book_delete(book_id: int):
    """Удалить книгу."""
    book_id -= 1

    if book_id < 0 or book_id >= len(books_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    result = books_list.pop(book_id)

    return {'message': f'Книга {result.title} была удалена'}
