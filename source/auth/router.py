from fastapi import APIRouter, Cookie, Depends, Response, status

from source.auth.auth import register_user, set_tokens_in_cookies
from source.auth.dependenties import get_current_user, verify_refresh_token
from source.auth.models import User
from source.auth.schemas import SUserLogin, SUserRegistration, SUserResponse, SUserSwitchPassword
from source.auth.service import UsersService

router = APIRouter(prefix="/users", tags=["Authenticate and Users"])


@router.post(path="", description="Registration user", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: SUserRegistration):
    await register_user(user_data)


@router.get(
    path="", response_model=SUserResponse, description="Get current User, need Session token"
)
async def get_auth_user(user: User = Depends(get_current_user)):
    return user


@router.patch(
    path="",
    description="Switch password, need Session token",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def switch_password_current_user(
    passwords: SUserSwitchPassword, user: User = Depends(get_current_user)
):
    await UsersService.switch_password(
        passwords.current_password, passwords.new_password, str(user.email)
    )


@router.post(path="/auth", description="Authenticate user")
async def login_user(response: Response, user_data: SUserLogin):
    user = await UsersService.authenticate_user(email=user_data.email, password=user_data.password)

    response, session_token, refresh_token = await set_tokens_in_cookies(response, str(user.id))


@router.get(path="/auth/refresh", description="Refresh session token")
async def refresh_tokens(
    response: Response, anonym_refresh_token: str = Cookie(description="Cookie for refresh tokens")
):
    user = await verify_refresh_token(anonym_refresh_token)
    response, session_token, refresh_token = await set_tokens_in_cookies(response, str(user.id))


@router.delete(
    path="/auth",
    description="Logout of the current user, need Session token",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(response: Response, user: User = Depends(get_current_user)):
    await UsersService.set_refresh_token_id(token_id="", user_id=user.id)

    response.delete_cookie("anonym_site_token")
    response.delete_cookie("anonym_refresh_token")
