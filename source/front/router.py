from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["Frontend"])

templates = Jinja2Templates(directory="source/front/templates")


@router.get("/", description="Main page", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
        },
    )


@router.get("/register", description="Register page", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", context={"request": request})


@router.get("/login", description="Login page", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})
