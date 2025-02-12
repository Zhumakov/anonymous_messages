from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["Frontend"])

templates = Jinja2Templates(directory="source/front/templates")

# Пример данных для передачи в шаблон
users = [
    {"user_uid": "user123", "about_me": "Люблю котиков!"},
    {"user_uid": "user456", "about_me": "Привет, мир!"},
]

messages = [
    {"sender": "user123", "date": "2023-10-27", "preview": "Привет!"},
    {"sender": "user456", "date": "2023-10-28", "preview": "Как дела?"},
]


@router.get("/", description="Main page", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "user": users[0],
            "messages": messages,
            "message_type": "recived",
        },
    )
