from fastapi import HTTPException, status

IsNotAuthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not is not authorized"
)

TokenValidException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired"
)

RefreshTokenIsInvalid = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Refresh token is invalid"
)

UserAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exist",
    headers={"field": "email"},
)

UsernameAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This username already exist",
    headers={"field": "usernames"},
)

UserCreateFail = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to create user"
)

AuthFailed = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password"
)

RefreshTokenCreateFailed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token is not created"
)
