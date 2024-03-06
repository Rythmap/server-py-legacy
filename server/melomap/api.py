from utils.validators import *
from utils.random_digits import *
from fastapi import APIRouter
from models.account_models import *
from configs.app_config import *
import uuid


router = APIRouter()

def create_access_token():
    return str(uuid.uuid4())

@router.post(
    f"{path_prefix_end}account.register",
    summary="Register a new account",
    response_description="The access token for the new account",
    responses={
        200: {
            "description": "The access token for the new account",
            "content": {
                "application/json": {
                    "example": {"access_token": "example_token", "token_type": "bearer"}
                }
            }
        },
        INVALID_USERNAME_OR_PASSWORD: {"description": INVALID_USERNAME_OR_PASSWORD_DETAIL},
        INVALID_USERNAME: {"description": INVALID_USERNAME_DETAIL},
        INVALID_USERNAME_LENGTH: {"description": INVALID_USERNAME_LENGTH_DETAIL},
        INVALID_PASSWORD_LENGTH: {"description": INVALID_PASSWORD_LENGTH_DETAIL},
        USERNAME_ALREADY_REGISTERED: {"description": USERNAME_ALREADY_REGISTERED_DETAIL},
        EMAIL_ALREADY_EXISTS: {"description": EMAIL_ALREADY_EXISTS_DETAIL},
    },
)
async def register(account: Account):
    validate_username(account.username)
    validate_username_length(account.username)
    validate_password_length(account.password)
    check_existing_username(account.username)

    if account.email != "":
        check_existing_email(account.email)

    hashed_password = pwd_context.hash(account.password)
    access_token = create_access_token()
    account_collection.insert_one(
        {
            "account_id": get_random_digits_str(32),
            "username": account.username,
            "password": hashed_password,
            "email": account.email,
            "token": access_token,
            "email_confirmed": False
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    f"{path_prefix_end}account.login",
    summary="Login to an account",
    response_description="The access token for the logged in account",
    responses={
        200: {
            "description": "The access token for the logged in account",
            "content": {
                "application/json": {
                    "example": {"access_token": "example_token", "token_type": "bearer"}
                }
            }
        },
        INVALID_USERNAME_OR_PASSWORD: {"description": INVALID_USERNAME_OR_PASSWORD_DETAIL},
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def login(account: AccountLogin):
    user = get_user_by_username_or_email(account.username)
    validate_user_credentials(user, account.password)
    return {"access_token": user["token"], "token_type": "bearer"}


@router.get(
    f"{path_prefix_end}account.info",
    summary="Get account info",
    response_description="The account info",
    responses={
        200: {
            "description": "The account info",
            "content": {
                "application/json": {
                    "example": {"token_valid": True, "username": "example_username", "email": "example@email.com", "email_confirmed": False}
                }
            }
        },
        INVALID_TOKEN: {"description": INVALID_TOKEN_DETAIL},
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def login(token: str):
    user = get_user_by_token(token)
    return {"token_valid": True, "username": user["username"], "email": user["email"],
            "email_confirmed": user["email_confirmed"]}

@router.post(
    f"{path_prefix_end}account.token.reset",
    summary="Reset account token",
    response_description="The new access token",
    responses={
        200: {
            "description": "The new access token",
            "content": {
                "application/json": {
                    "example": {"access_token": "new_example_token", "token_type": "bearer"}
                }
            }
        },
        INVALID_USERNAME_OR_PASSWORD: {"description": INVALID_USERNAME_OR_PASSWORD_DETAIL},
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def reset_token(account: AccountLogin):
    user = get_user_by_username(account.username)
    validate_user_credentials(user, account.password)

    new_token = create_access_token()
    account_collection.update_one(
        {"username": account.username}, {"$set": {"token": new_token}}
    )
    return {"access_token": new_token, "token_type": "bearer"}

@router.post(
    f"{path_prefix_end}account.changenick",
    summary="Change account nickname",
    response_description="The status of the nickname change",
    responses={
        200: {
            "description": "The status of the nickname change",
            "content": {
                "application/json": {
                    "example": {"status": "username changed"}
                }
            }
        },
        INVALID_USERNAME: {"description": INVALID_USERNAME_DETAIL},
        INVALID_USERNAME_LENGTH: {"description": INVALID_USERNAME_LENGTH_DETAIL},
        USERNAME_ALREADY_REGISTERED: {"description": USERNAME_ALREADY_REGISTERED_DETAIL},
        USERNAME_CHANGE_FAILED: {"description": USERNAME_CHANGE_FAILED_DETAIL},
    },
)
async def change_nickname(change_nickname: ChangeNickname):
    validate_username(change_nickname.new_username)
    validate_username_length(change_nickname.new_username)
    check_existing_username(change_nickname.new_username)

    result = account_collection.update_one(
        {"token": change_nickname.token}, {"$set": {"username": change_nickname.new_username}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=USERNAME_CHANGE_FAILED, detail=USERNAME_CHANGE_FAILED_DETAIL)

    return {"status": "username changed"}


@router.post(
    f"{path_prefix_end}account.changepswd",
    summary="Change account password",
    response_description="The status of the password change",
    responses={
        200: {
            "description": "The status of the password change",
            "content": {
                "application/json": {
                    "example": {"status": "password changed"}
                }
            }
        },
        INVALID_USERNAME_OR_PASSWORD: {"description": INVALID_USERNAME_OR_PASSWORD_DETAIL},
        INVALID_PASSWORD_LENGTH: {"description": INVALID_PASSWORD_LENGTH_DETAIL},
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def change_password(change_password: ChangePassword):
    user = get_user_by_username(change_password.username)
    validate_user_credentials(user, change_password.current_password)
    validate_password_length(change_password.new_password)

    hashed_password = pwd_context.hash(change_password.new_password)
    account_collection.update_one(
        {"username": change_password.username}, {"$set": {"password": hashed_password}}
    )
    return {"status": "password changed"}


@router.delete(
    f"{path_prefix_end}account.delete",
    summary="Delete an account",
    response_description="The status of the account deletion",
    responses={
        200: {
            "description": "The status of the account deletion",
            "content": {
                "application/json": {
                    "example": {"status": "account deleted"}
                }
            }
        },
        INVALID_USERNAME_OR_PASSWORD: {"description": INVALID_USERNAME_OR_PASSWORD_DETAIL},
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def delete_account(account: AccountLogin):
    user = get_user_by_username(account.username)
    validate_user_credentials(user, account.password)
    account_collection.delete_one(user)
    return {"status": "account deleted"}