import uvicorn
from fastapi import FastAPI
from routers.main_page import router as main_pages_router
from routers.crud_books import router as crud_books_router
from routers.books_html import router as books_html


app = FastAPI()
app.include_router(main_pages_router, tags=["Main pages"])
app.include_router(crud_books_router, tags=[
                   "Crud books"], prefix="/api/v1/books")
app.include_router(books_html, tags=["Books html"], prefix="/books")

if __name__ == '__main__':
    uvicorn.run('app:app', host="127.0.0.1", port=8000, reload=True)
