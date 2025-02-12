from fastapi import FastAPI

from source.exceptions.auth_exc import exc_handlers as auth_handlers
from source.exceptions.auth_exc import exceptions as auth_excs
from source.exceptions.messages_exc import exc_handlers as messages_handlers
from source.exceptions.messages_exc import exceptions as message_excs


def bind_auth_exc_handlers_with_app(app: FastAPI):
    app.add_exception_handler(auth_excs.ExistingUserException, auth_handlers.exist_user_exc_handler)
    app.add_exception_handler(
        auth_excs.ExistingUsernameException, auth_handlers.exist_username_exc_handler
    )
    app.add_exception_handler(auth_excs.UserCreateException, auth_handlers.user_create_exc_handler)
    app.add_exception_handler(
        auth_excs.UserIsNotExistException, auth_handlers.user_is_not_exist_exc_handler
    )
    app.add_exception_handler(
        auth_excs.PasswordChangeException, auth_handlers.pass_change_exc_handler
    )
    app.add_exception_handler(
        auth_excs.PasswordIsInvalidException, auth_handlers.pass_is_not_valid_exc_handler
    )
    app.add_exception_handler(
        auth_excs.RefreshTokenIdIsNotValidException,
        auth_handlers.refresh_token_id_is_not_valid_exc_handler,
    )
    app.add_exception_handler(
        auth_excs.RefreshTokenSetException, auth_handlers.refresh_token_set_exc_handler
    )
    app.add_exception_handler(auth_excs.TokenDataException, auth_handlers.token_data_exc_hander)
    app.add_exception_handler(auth_excs.TokenValidException, auth_handlers.token_valid_exc_handler)


def bind_messages_exc_handlers_with_app(app: FastAPI):
    app.add_exception_handler(
        message_excs.MessageCreateException, messages_handlers.message_create_exc_handler
    )
    app.add_exception_handler(
        message_excs.MessageVerifyException, messages_handlers.message_verify_exc_handler
    )
    app.add_exception_handler(
        message_excs.NotSentMessageToMyselfException,
        messages_handlers.not_sent_message_to_yourself_exc_handler,
    )
