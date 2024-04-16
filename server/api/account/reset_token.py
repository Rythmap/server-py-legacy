from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.token import create_access_token
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()

@router.post(
    f"{path_prefix_end}account.reset.token",
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
        INVALID_NICKNAME_OR_PASSWORD: {
            "description": INVALID_NICKNAME_OR_PASSWORD_DETAIL
        },
        NO_USER: {"description": NO_USER_DETAIL},
    },
)
async def reset_token(account: ResetToken):
    """Reset account token

    Resets the account's authentication token and returns the new token

    Args:
        account (AccountLogin): The account information, containing nickname and password

    Raises:
        HTTPException: If the nickname or password is invalid, or if the account does not exist

    Returns:
        dict: The new access token with the token type
    """
    user = get_user_by_nickname(account.nickname)
    validate_user_credentials(user, account.password)

    new_token = create_access_token()
    account_collection.update_one(
        {"nickname": account.nickname}, {"$set": {"token": new_token}}
    )

    return {"access_token": new_token, "token_type": "bearer"}

