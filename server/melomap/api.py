from utils.validators import *
from utils.random_digits import *
from fastapi import APIRouter
from models.account_models import *
from configs.app_config import *
import uuid


router = APIRouter()




def create_access_token() -> str:
    """
    Creates a new access token

    Returns:
        The new access token
    """
    return str(uuid.uuid4())


@router.post(
    f"{path_prefix_end}account.register",
    summary="Register a new account",
    description="Registers a new account in the database and returns an access token",
    response_description="The access token for the new account",
    responses={
        200: {
            "description": "The access token for the new account",
            "content": {
                "application/json": {
                    "example": {"access_token": "example_token", "token_type": "bearer"}
                }
            },
        },
        INVALID_USERNAME_OR_PASSWORD: {
            "description": INVALID_USERNAME_OR_PASSWORD_DETAIL
        },
        INVALID_USERNAME: {"description": INVALID_USERNAME_DETAIL},
        INVALID_USERNAME_LENGTH: {"description": INVALID_USERNAME_LENGTH_DETAIL},
        INVALID_PASSWORD_LENGTH: {"description": INVALID_PASSWORD_LENGTH_DETAIL},
        USERNAME_ALREADY_REGISTERED: {
            "description": USERNAME_ALREADY_REGISTERED_DETAIL
        },
        EMAIL_ALREADY_EXISTS: {"description": EMAIL_ALREADY_EXISTS_DETAIL},
    },
)
async def register(account: Account):
    """Register a new account

    Args:
        account (Account): The account information, containing username, password, and optional email

    Raises:
        HTTPException: If the username or password is invalid, if the username is already taken, or if the email is already in use

    Returns:
        dict: The access token for the new account with the token type
    """
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
            "email_confirmed": False,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    f"{path_prefix_end}account.login",
    summary="Login to an account",
    description="Logs in to an account given the username and password",
    response_description="The access token for the logged in account",
    responses={
        200: {
            "description": "The access token for the logged in account",
            "content": {
                "application/json": {
                    "example": {"access_token": "example_token", "token_type": "bearer"}
                }
            },
        },
        INVALID_USERNAME_OR_PASSWORD: {
            "description": INVALID_USERNAME_OR_PASSWORD_DETAIL
        },
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def login(account: AccountLogin):
    """Logs in to an account

    Args:
        account (AccountLogin): The account information, containing username and password

    Raises:
        HTTPException: If the username or password is invalid, or if the account does not exist

    Returns:
        dict: The access token for the logged in account with the token type
    """
    user = get_user_by_username_or_email(account.username)
    validate_user_credentials(user, account.password)
    return {"access_token": user["token"], "token_type": "bearer"}


@router.get(
    f"{path_prefix_end}account.info",
    summary="Get account info",
    responses={
        200: {"content": {"application/json": {}}},
        401: {"description": INVALID_TOKEN_DETAIL},
        404: {"description": NO_USER_DETAIL},
    },
)
async def get_account_info(token: str):
    """Get account info"""
    user = get_user_by_token(token)
    return {
        "username": user["username"],
        "email": user["email"],
        "email_confirmed": user["email_confirmed"],
    }


@router.post(
    f"{path_prefix_end}account.token.reset",
    summary="Reset account token",
    description="Resets the account's authentication token and returns the new token",
    response_description="The new access token",
    responses={
        200: {
            "description": "The new access token",
            "content": {
                "application/json": {
                    "example": {"access_token": "new_token", "token_type": "bearer"}
                }
            },
        },
        INVALID_USERNAME_OR_PASSWORD: {
            "description": INVALID_USERNAME_OR_PASSWORD_DETAIL
        },
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def reset_token(account: AccountLogin):
    """Reset account token

    Resets the account's authentication token and returns the new token

    Args:
        account (AccountLogin): The account information, containing username and password

    Raises:
        HTTPException: If the username or password is invalid, or if the account does not exist

    Returns:
        dict: The new access token with the token type
    """
    user = get_user_by_username(account.username)
    validate_user_credentials(user, account.password)

    new_token = create_access_token()
    account_collection.update_one(
        {"username": account.username}, {"$set": {"token": new_token}}
    )

    return {"access_token": new_token, "token_type": "bearer"}


@router.post(
    f"{path_prefix_end}account.changeusername",
    summary="Change account username",
    description="Changes the account's username",
    response_description="The status of the username change",
    responses={
        200: {
            "description": "The status of the username change",
            "content": {
                "application/json": {"example": {"status": "username changed"}}
            },
        },
        INVALID_USERNAME: {
            "description": INVALID_USERNAME_DETAIL,
        },
        INVALID_USERNAME_LENGTH: {
            "description": INVALID_USERNAME_LENGTH_DETAIL,
        },
        USERNAME_ALREADY_REGISTERED: {
            "description": USERNAME_ALREADY_REGISTERED_DETAIL,
        },
        USERNAME_CHANGE_FAILED: {
            "description": USERNAME_CHANGE_FAILED_DETAIL,
        },
    },
)
async def change_username(change_username: ChangeUsername):
    """Change account username

    Validates the new username, checks if it's already registered, and changes the
    account's username

    Args:
        change_username (ChangeUsername): The new username

    Returns:
        dict: The status of the username change

    Raises:
        HTTPException: If the username is invalid, already registered, or could
            not be changed
    """
    validate_username(change_username.new_username)
    validate_username_length(change_username.new_username)
    check_existing_username(change_username.new_username)

    result = account_collection.update_one(
        {"token": change_username.token},
        {"$set": {"username": change_username.new_username}},
    )
    if not result.modified_count:
        raise HTTPException(status_code=400, detail="Username change failed")

    return {"status": "username changed"}


@router.post(
    f"{path_prefix_end}account.changepswd",
    summary="Change account password",
    description="Changes the password of the authenticated user",
    response_description="The status of the password change",
    responses={
        200: {
            "description": "The status of the password change",
            "content": {
                "application/json": {"example": {"status": "password changed"}}
            },
        },
        INVALID_USERNAME_OR_PASSWORD: {
            "description": INVALID_USERNAME_OR_PASSWORD_DETAIL,
        },
        INVALID_PASSWORD_LENGTH: {
            "description": INVALID_PASSWORD_LENGTH_DETAIL,
        },
        NO_USER: {
            "description": NO_USER_DETAIL,
        },
    },
)
async def change_password(change_password: ChangePassword):
    """Change the password of an existing user

    Args:
        change_password (ChangePassword): The username, current password and new password

    Returns:
        dict: The status of the password change
    """
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
    description="Deletes the account of the user",
    responses={
        200: {
            "description": "The status of the account deletion",
            "content": {"application/json": {"example": {"status": "account deleted"}}},
        },
        INVALID_TOKEN: {"description": INVALID_TOKEN_DETAIL},
    },
)
async def delete_account(account: AccountLogin):
    """Delete an existing account

    Args:
        account (AccountLogin): The username and password of the account to delete

    Returns:
        dict: The status of the account deletion
    """
    user = get_user_by_username(account.username)
    # Verify the credentials of the user
    validate_user_credentials(user, account.password)
    # Delete the account from the database
    account_collection.delete_one({"_id": user["_id"]})
    return {"status": "account deleted"}
