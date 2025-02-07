from fastapi import HTTPException, status

ExistingUserHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with this alredy exist"
)

ExistingUsernameHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with this username alredy exist"
)

UnauthorizedHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not autorized"
)

TokenValidHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid or he has expire"
)

TokenDataHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing data information in token"
)

UserIsNotExistHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not registred"
)

PasswordIsInvalidHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is invalid"
)

RefreshTokenIdIsNotValidHTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Refresh token id is not valid, or the user is logged out",
)

MessageVerifyHTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="You have not received this message"
)

# -------------------------------------------------------------------------

MessageCreateHTTPException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Couldn't send message"
)

ServerError = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
