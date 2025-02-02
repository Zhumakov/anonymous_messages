from email.message import EmailMessage

import aiosmtplib

from source.auth.service import UsersService
from source.settings import settings


def create_message_for_register(message_to: str, user_id: int) -> EmailMessage:
    token = UsersService.create_token_for_register(user_id)
    unique_url = f"{settings.API_ADRESS}/auth/register?token={token}"
    body = f"""
           Перейдите по ссылке ниже чтобы зарегестрироваться на сервисе анонимных сообщений\n\n
           {unique_url}\n\n
           Если это были не вы, проигнорируйте это сообщение
           """

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = message_to
    message.set_content(body)
    return message


async def send_email(message: EmailMessage) -> bool:
    async with aiosmtplib.SMTP(hostname=settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
        await smtp.auth_login(settings.SMTP_USER, settings.SMTP_PASS)
        await smtp.send_message(message)
        return True
