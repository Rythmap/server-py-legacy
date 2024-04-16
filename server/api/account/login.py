from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()

@router.post(
    f"{path_prefix_end}account.login",
    summary="Login to an account",
    description="Logs in to an account given the nickname and password",
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
        INVALID_NICKNAME_OR_PASSWORD: {
            "description": INVALID_NICKNAME_OR_PASSWORD_DETAIL
        },
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def login(account: Login):
    """Logs in to an account

    Args:
        account (Login): The account information, containing nickname and password

    Raises:
        HTTPException: If the nickname or password is invalid, or if the account does not exist

    Returns:
        dict: The access token for the logged in account with the token type
    """
    user = get_user_by_nickname_or_email(account.nickname)
    validate_user_credentials(user, account.password)
    return {"access_token": user["token"], "token_type": "bearer"}
