from re import U
from fastapi import APIRouter, HTTPException, Response, status
from jose.exceptions import JWTError

from source.auth.service import UsersService
from source.auth.schemas import SUserLogin, SUserRequest
from source.auth.auth import get_hash_password, create_session_token


router = APIRouter(prefix="/users", tags=["Authenticate and Users"])


@router.post(path="", description="Registration user", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: SUserRequest):
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

    hashed_password = get_hash_password(user_data.password)
    await UsersService.insert_into_table(
        username=user_data.username, email=user_data.email, hashed_password=hashed_password
    )


@router.get(path="", description="Get current User, need Session token")
async def get_current_user():
    pass


@router.delete(path="", description="Delete current user, need Session token")
async def delete_current_user():
    pass


@router.patch(path="", description="Switch password, need Session token")
async def switch_password_current_user():
    pass


@router.post(path="/auth", description="Authenticate user")
async def auth_user(response: Response, user_data: SUserLogin):
    user = await UsersService.get_one_or_none(email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not autorized"
        )

    session_token = create_session_token(sub=user_data.email)
    response.set_cookie("anonym_site_token", session_token, httponly=True)
    return {"anonym_site_token": session_token}


@router.delete(path="/auth", description="Logout current user, need Session token")
async def logout_user():
    pass
