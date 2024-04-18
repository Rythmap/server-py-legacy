
import re
from fastapi import HTTPException

from utils.config_parser import *
from utils.errors import *

def validate_nickname(nickname: str):
    if not re.match("^[a-zA-Z0-9]*$", nickname):
        raise HTTPException(
            status_code=INVALID_NICKNAME,
            detail=INVALID_NICKNAME_DETAIL,
        )


def validate_nickname_length(nickname: str):
    if len(nickname) < 3 or len(nickname) > 32:
        raise HTTPException(
            status_code=INVALID_NICKNAME_LENGTH,
            detail=INVALID_NICKNAME_LENGTH_DETAIL,
        )


def validate_password_length(password: str):
    if len(password) < 6 or len(password) > 64:
        raise HTTPException(
            status_code=INVALID_PASSWORD_LENGTH,
            detail=INVALID_PASSWORD_LENGTH_DETAIL,
        )


def check_existing_nickname(nickname: str):
    if account_collection.find_one({"nickname": nickname}):
        raise HTTPException(
            status_code=NICKNAME_ALREADY_REGISTERED,
            detail=NICKNAME_ALREADY_REGISTERED_DETAIL,
        )


def get_user_by_nickname(nickname: str):
    user = account_collection.find_one({"nickname": nickname})
    if not user:
        raise HTTPException(status_code=NO_USER, detail=NO_USER_DETAIL)
    return user


def get_user_by_token(token: str):
    user = account_collection.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=INVALID_TOKEN, detail=INVALID_TOKEN_DETAIL)
    return user


def get_user_by_recovery_token(recovery_token: str):
    user = recovery_token_collection.find_one({"recovery_token": recovery_token})
    if not user:
        raise HTTPException(status_code=INVALID_RECOVERY_TOKEN, detail=INVALID_RECOVERY_TOKEN_DETAIL)
    return user


def get_user_by_confirm_token(confirm_token: str):
    user = confirm_token_collection.find_one({"confirm_token": confirm_token})
    if not user:
        raise HTTPException(status_code=INVALID_CONFIRM_TOKEN, detail=INVALID_CONFIRM_TOKEN_DETAIL)
    return user


def validate_user_credentials(user, password):
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=INVALID_NICKNAME_OR_PASSWORD, detail=INVALID_NICKNAME_OR_PASSWORD_DETAIL)


def check_existing_email(email: str):
    account = account_collection.find_one({"email": email})
    if account is not None:
        raise HTTPException(status_code=EMAIL_ALREADY_EXISTS, detail=EMAIL_ALREADY_EXISTS_DETAIL)


def check_email_confirmed(user):
    email_confirmed = user["email_confirmed"]
    if email_confirmed:
        raise HTTPException(status_code=EMAIL_ALREADY_CONFIRMED, detail=EMAIL_ALREADY_CONFIRMED_DETAIL)


def get_user_by_nickname_or_email(nickname):
    if "@" in nickname:
        user = account_collection.find_one({"email": nickname})
    else:
        user = account_collection.find_one({"nickname": nickname})
    if not user:
        raise HTTPException(status_code=INVALID_NICKNAME_OR_EMAIL, detail=INVALID_NICKNAME_OR_EMAIL_DETAIL)
    return user
