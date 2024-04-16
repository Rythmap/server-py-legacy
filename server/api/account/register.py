from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.token import create_access_token
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()



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
        INVALID_NICKNAME_OR_PASSWORD: {
            "description": INVALID_NICKNAME_OR_PASSWORD_DETAIL
        },
        INVALID_NICKNAME: {"description": INVALID_NICKNAME_DETAIL},
        INVALID_NICKNAME_LENGTH: {"description": INVALID_NICKNAME_LENGTH_DETAIL},
        INVALID_PASSWORD_LENGTH: {"description": INVALID_PASSWORD_LENGTH_DETAIL},
        NICKNAME_ALREADY_REGISTERED: {
            "description": NICKNAME_ALREADY_REGISTERED_DETAIL
        },
        EMAIL_ALREADY_EXISTS: {"description": EMAIL_ALREADY_EXISTS_DETAIL},
    },
)
async def register(account: Register):
    """Register a new account

    Args:
        account (Register): The account information, containing nickname, password, and optional email

    Raises:
        HTTPException: If the nickname or password is invalid, if the nickname is already taken, or if the email is already in use

    Returns:
        dict: The access token for the new account with the token type
    """
    validate_nickname(account.nickname)
    validate_nickname_length(account.nickname)
    validate_password_length(account.password)
    check_existing_nickname(account.nickname)

    if account.email != "":
        check_existing_email(account.email)

    hashed_password = pwd_context.hash(account.password)
    access_token = create_access_token()
    account_collection.insert_one(
        {
            "account_id": get_random_digits_str(32),
            "nickname": account.nickname,
            "password": hashed_password,
            "email": account.email,
            "token": access_token,
            "email_confirmed": False,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
