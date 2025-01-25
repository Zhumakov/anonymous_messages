from fastapi import APIRouter, Depends, HTTPException, Response, status

from source.auth.auth import register_user, set_tokens_in_cookies
from source.auth.dependenties import get_current_user, get_refresh_token, verify_refresh_token
from source.auth.models import Users
from source.auth.schemas import SUserLogin, SUserRegistration, SUserResponse
from source.auth.service import UsersService

router = APIRouter(prefix="/users", tags=["Authenticate and Users"])


@router.post(path="", description="Registration user", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: SUserRegistration):
    existing_user = await UsersService.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with this alredy exist"
        )

    existing_username = await UsersService.get_one_or_none(username=user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with this username alredy exist"
        )
    await register_user(user_data)


@router.get(
    path="", response_model=SUserResponse, description="Get current User, need Session token"
)
async def get_auth_user(user: Users = Depends(get_current_user)):
    return user


@router.patch(path="", description="Switch password, need Session token")
async def switch_password_current_user():
    pass


@router.post(path="/auth", description="Authenticate user")
async def login_user(response: Response, user_data: SUserLogin):
    user = await UsersService.authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not autorized"
        )

    response, session_token, refresh_token = await set_tokens_in_cookies(response, str(user.id))
    return {"anonym_site_token": session_token, "anonym_refresh_token": refresh_token}


@router.get(path="/auth/refresh", description="Refresh session token")
async def refresh_tokens(response: Response, refresh_token: str = Depends(get_refresh_token)):
    if not (user := await verify_refresh_token(refresh_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token id is invalid"
        )

    response, session_token, refresh_token = await set_tokens_in_cookies(response, str(user.id))
    return {"anonym_site_token": session_token, "anonym_refresh_token": refresh_token}


@router.delete(
    path="/auth",
    description="Logout of the current user, need Session token",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(response: Response):
    response.delete_cookie("anonym_site_token")
    response.delete_cookie("anonym_refresh_token")
