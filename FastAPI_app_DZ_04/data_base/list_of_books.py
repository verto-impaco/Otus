from pydantic import BaseModel


class Books(BaseModel):
    title: str
    author: str
    year: int
    id: int


books_list = [
    Books(
        title='Lord of the Rings',
        author='J.R.R. Tolkien',
        year=1937,
        id=1,
    ),
    Books(
        title='War and Peace',
        author='Tolstoy',
        year=1863,
        id=2,
    ),
    Books(
        title='Lefty',
        author='Leskov',
        year=1881,
        id=3,
    ),

]
