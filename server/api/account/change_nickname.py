from fastapi import APIRouter

from utils.config_parser import *
from models.account_models import *
from utils.random_digits import *
from utils.validators import *
from utils.errors import *
router = APIRouter()


@router.post(
    f"{path_prefix_end}account.changenickname",
    summary="Change account nickname",
    description="Changes the account's nickname",
    response_description="The status of the nickname change",
    responses={
        200: {
            "description": "The status of the nickname change",
            "content": {
                "application/json": {"example": {"status": "nickname changed"}}
            },
        },
        INVALID_NICKNAME: {
            "description": INVALID_NICKNAME_DETAIL,
        },
        INVALID_NICKNAME_LENGTH: {
            "description": INVALID_NICKNAME_LENGTH_DETAIL,
        },
        NICKNAME_ALREADY_REGISTERED: {
            "description": NICKNAME_ALREADY_REGISTERED_DETAIL,
        },
        NICKNAME_CHANGE_FAILED: {
            "description": NICKNAME_CHANGE_FAILED_DETAIL,
        },
    },
)
async def change_nickname(change_nickname: ChangeNickname):
    """Change account nickname

    Validates the new nickname, checks if it's already registered, and changes the
    account's nickname

    Args:
        change_nickname (ChangeNickname): The new nickname

    Returns:
        dict: The status of the nickname change

    Raises:
        HTTPException: If the nickname is invalid, already registered, or could
            not be changed
    """
    validate_nickname(change_nickname.new_nickname)
    validate_nickname_length(change_nickname.new_nickname)
    check_existing_nickname(change_nickname.new_nickname)

    result = account_collection.update_one(
        {"token": change_nickname.token},
        {"$set": {"nickname": change_nickname.new_nickname}},
    )
    if not result.modified_count:
        raise HTTPException(status_code=400, detail="Nickname change failed")

    return {"status": "nickname changed"}
