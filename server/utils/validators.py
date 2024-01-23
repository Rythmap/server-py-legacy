from configs.errors import *
import re
from fastapi import HTTPException
from configs.mongo import *

def validate_username(username: str):
    if not re.match("^[a-zA-Z0-9]*$", username):
        raise HTTPException(
            status_code=INVALID_USERNAME,
            detail=INVALID_USERNAME_DETAIL,
        )


def validate_username_length(username: str):
    if len(username) < 3 or len(username) > 32:
        raise HTTPException(
            status_code=INVALID_USERNAME_LENGTH,
            detail=INVALID_USERNAME_LENGTH_DETAIL,
        )


def validate_password_length(password: str):
    if len(password) < 6 or len(password) > 64:
        raise HTTPException(
            status_code=INVALID_PASSWORD_LENGTH,
            detail=INVALID_PASSWORD_LENGTH_DETAIL,
        )


def check_existing_username(username: str):
    if account_collection.find_one({"username": username}):
        raise HTTPException(
            status_code=USERNAME_ALREADY_REGISTERED,
            detail=USERNAME_ALREADY_REGISTERED_DETAIL,
        )


def get_user_by_username(username: str):
    user = account_collection.find_one({"username": username})
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
        raise HTTPException(status_code=INVALID_USERNAME_OR_PASSWORD, detail=INVALID_USERNAME_OR_PASSWORD_DETAIL)


def check_existing_email(email: str):
    account = account_collection.find_one({"email": email})
    if account is not None:
        raise HTTPException(status_code=EMAIL_ALREADY_EXISTS, detail=EMAIL_ALREADY_EXISTS_DETAIL)


def check_email_confirmed(user):
    email_confirmed = user["email_confirmed"]
    if email_confirmed:
        raise HTTPException(status_code=EMAIL_ALREADY_CONFIRMED, detail=EMAIL_ALREADY_CONFIRMED_DETAIL)


def get_user_by_username_or_email(username):
    if "@" in username:
        user = account_collection.find_one({"email": username})
    else:
        user = account_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=INVALID_USERNAME_OR_EMAIL, detail=INVALID_USERNAME_OR_EMAIL_DETAIL)
    return user