from fastapi import APIRouter

from models.account_models import *
from utils.random_digits import *
from utils.validators import *
from utils.config_parser import *
from utils.errors import *

router = APIRouter()


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
        INVALID_NICKNAME_OR_PASSWORD: {
            "description": INVALID_NICKNAME_OR_PASSWORD_DETAIL,
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
        change_password (ChangePassword): The nickname, current password and new password

    Returns:
        dict: The status of the password change
    """
    user = get_user_by_nickname(change_password.nickname)

    validate_user_credentials(user, change_password.current_password)
    validate_password_length(change_password.new_password)

    hashed_password = pwd_context.hash(change_password.new_password)
    account_collection.update_one(
        {"nickname": change_password.nickname}, {"$set": {"password": hashed_password}}
    )

    return {"status": "password changed"}
