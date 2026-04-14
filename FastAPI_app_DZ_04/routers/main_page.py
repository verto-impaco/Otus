from fastapi import APIRouter
from pathlib import Path
from dataclasses import dataclass
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from data_base.list_of_books import books_list


router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@dataclass
class Developer:
    name: str
    age: int


@router.get("/", response_class=HTMLResponse, name='main_page')
async def index(request: Request):

    context = {
        'request': request,
        'list_of_books': books_list,
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@router.get('/about/', response_model=Developer, name='about_us')
async def about(request: Request):
    about = Developer('Vasiliy', 21)

    about_us = {
        "request": request,
        'name': about.name,
        'age': about.age,
    }

    return templates.TemplateResponse(
        request=request,
        name="about_us.html",
        context=about_us

    )
