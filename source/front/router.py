from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from source.auth.dependenties import get_current_user
from source.exceptions.auth_exc import exceptions

router = APIRouter(prefix="", tags=["Frontend"])

templates = Jinja2Templates(directory="source/front/templates")


@router.get("/", description="Main page", response_class=HTMLResponse)
async def main_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("anonym_site_token"))
    except exceptions.IsNotAuthorized:
        return RedirectResponse("/register")

    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get("/register", description="Register page", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", context={"request": request})


@router.get("/login", description="Login page", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})
