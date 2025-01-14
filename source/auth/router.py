from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["Authenticate and Users"])


@router.post(path="", description="Registration user")
async def create_user():
    pass


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
async def auth_user():
    pass


@router.delete(path="/auth", description="Logout current user, need Session token")
async def logout_user():
    pass
