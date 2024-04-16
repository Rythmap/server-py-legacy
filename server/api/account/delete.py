from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()


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
async def delete_account(account: DeleteAccount):
    """Delete an existing account

    Args:
        account (AccountLogin): The nickname and password of the account to delete

    Returns:
        dict: The status of the account deletion
    """
    user = get_user_by_nickname(account.nickname)
    # Verify the credentials of the user
    validate_user_credentials(user, account.password)
    # Delete the account from the database
    account_collection.delete_one({"_id": user["_id"]})
    return {"status": "account deleted"}
